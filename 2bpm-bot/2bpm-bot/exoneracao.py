import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta

OWNER_ID = 000  # Seu ID
CARGO_FIXO_ID = 000  # Cargo fixo que será mencionado
CANAL_FIXO_ID = 000  # Canal fixo onde a embed será enviada
ARQUIVO_JSON = "exoneracoes.json"  # Para salvar os agendamentos de expulsão
TEMPO_EXPULSAR_HORAS = 2  # Tempo até expulsar o membro (2 horas)


class Exonerar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.exoneracoes = self.carregar_dados()
        self.verificar_expulsoes.start()

    def carregar_dados(self):
        if os.path.exists(ARQUIVO_JSON):
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def salvar_dados(self):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(self.exoneracoes, f, indent=4, ensure_ascii=False)

    @tasks.loop(minutes=5)
    async def verificar_expulsoes(self):
        agora = datetime.utcnow()
        for guild_id, membros in list(self.exoneracoes.items()):
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
            for membro_id, data_str in list(membros.items()):
                data_expulsao = datetime.fromisoformat(data_str)
                if agora >= data_expulsao:
                    membro = guild.get_member(int(membro_id))
                    if membro:
                        try:
                            await membro.kick(
                                reason="Expulsão automática após exoneração"
                            )
                        except discord.Forbidden:
                            pass  # Sem permissão pra expulsar
                        except discord.HTTPException:
                            pass  # Erro na API
                    del self.exoneracoes[guild_id][membro_id]
            if not self.exoneracoes[guild_id]:
                del self.exoneracoes[guild_id]
        self.salvar_dados()

    # Autocomplete para membros
    async def autocomplete_membros(
        self, interaction: discord.Interaction, current: str
    ):
        membros = []
        for member in interaction.guild.members:
            if current.lower() in member.display_name.lower():
                membros.append(
                    app_commands.Choice(name=member.display_name, value=str(member.id))
                )
        return membros[:25]

    # Autocomplete para patentes
    async def autocomplete_patentes(
        self, interaction: discord.Interaction, current: str
    ):
        patentes = []
        for role in interaction.guild.roles:
            if current.lower() in role.name.lower():
                patentes.append(app_commands.Choice(name=role.name, value=str(role.id)))
        return patentes[:25]

    @app_commands.command(
        name="exonerar",
        description="Registrar uma exoneração e expulsar o membro após 2h (somente para uso autorizado).",
    )
    @app_commands.describe(
        qra="Selecione o militar (QRA)",
        patente="Selecione a patente",
        distintivo="Número ou código do distintivo",
        motivo="Motivo da exoneração",
    )
    @app_commands.autocomplete(qra=autocomplete_membros, patente=autocomplete_patentes)
    async def exonerar(
        self,
        interaction: discord.Interaction,
        qra: str,
        patente: str,
        distintivo: str,
        motivo: str,
    ):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        guild = interaction.guild
        cargo_fixo = guild.get_role(CARGO_FIXO_ID)
        membro = guild.get_member(int(qra))
        role_patente = guild.get_role(int(patente))
        canal_fixo = guild.get_channel(CANAL_FIXO_ID)

        embed = discord.Embed(title="📢 Registro de Exoneração!", color=0xFF0000)
        embed.add_field(
            name="**QRA:**",
            value=membro.display_name if membro else "Desconhecido",
            inline=False,
        )
        embed.add_field(
            name="**Patente:**",
            value=role_patente.name if role_patente else "Desconhecida",
            inline=False,
        )
        embed.add_field(name="**Distintivo:**", value=distintivo, inline=False)
        embed.add_field(name="**Motivo:**", value=motivo, inline=False)
        embed.set_footer(
            text=f"Exoneração registrada por {interaction.user.display_name}"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1388215342601605150/1399006385957638214/CDA_-_LOGO_2BPM_Dos_Anjos-1.png"
        )

        if canal_fixo:
            await canal_fixo.send(f"{cargo_fixo.mention}", embed=embed)
            # Agenda expulsão para daqui 2 horas
            data_expulsao = datetime.utcnow() + timedelta(hours=TEMPO_EXPULSAR_HORAS)
            self.exoneracoes.setdefault(str(guild.id), {})[
                str(membro.id)
            ] = data_expulsao.isoformat()
            self.salvar_dados()
            await interaction.response.send_message(
                f"✅ Exoneração registrada! O membro será expulso em {TEMPO_EXPULSAR_HORAS} horas.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ Canal fixo não encontrado. Verifique o ID.", ephemeral=True
            )

    @verificar_expulsoes.before_loop
    async def before_verificar_expulsoes(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Exonerar(bot))
