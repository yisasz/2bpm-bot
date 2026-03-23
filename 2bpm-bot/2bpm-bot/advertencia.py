import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta

OWNER_ID = 000  # Seu ID
CARGO_FIXO_ID = 000  # Cargo fixo que será mencionado
CANAL_FIXO_ID = 000  # Canal fixo onde a embed será enviada
CARGO_ADV_ID = 000  # Cargo de "Advertido"
DIAS_REMOVER = 7  # Quantos dias até remover o cargo ADV
ARQUIVO_JSON = "advertencias.json"  # Arquivo onde salva os prazos

class Advertencia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.advertencias = self.carregar_dados()
        self.verificar_remocoes.start()

    def carregar_dados(self):
        if os.path.exists(ARQUIVO_JSON):
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def salvar_dados(self):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(self.advertencias, f, indent=4, ensure_ascii=False)

    @tasks.loop(minutes=60)  # Checa a cada 1 hora
    async def verificar_remocoes(self):
        agora = datetime.utcnow()
        for guild_id, membros in list(self.advertencias.items()):
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
            for membro_id, data_str in list(membros.items()):
                data_remocao = datetime.fromisoformat(data_str)
                if agora >= data_remocao:
                    membro = guild.get_member(int(membro_id))
                    cargo_adv = guild.get_role(CARGO_ADV_ID)
                    if membro and cargo_adv in membro.roles:
                        try:
                            await membro.remove_roles(cargo_adv, reason="Remoção automática da advertência")
                        except discord.Forbidden:
                            pass
                    del self.advertencias[guild_id][membro_id]
            if not self.advertencias[guild_id]:
                del self.advertencias[guild_id]
        self.salvar_dados()

    # Autocomplete para membros
    async def autocomplete_membros(self, interaction: discord.Interaction, current: str):
        membros = []
        for member in interaction.guild.members:
            if current.lower() in member.display_name.lower():
                membros.append(app_commands.Choice(name=member.display_name, value=str(member.id)))
        return membros[:25]

    # Autocomplete para patentes
    async def autocomplete_patentes(self, interaction: discord.Interaction, current: str):
        patentes = []
        for role in interaction.guild.roles:
            if current.lower() in role.name.lower():
                patentes.append(app_commands.Choice(name=role.name, value=str(role.id)))
        return patentes[:25]

    @app_commands.command(name="advertencia", description="Registrar uma advertência militar (somente para uso autorizado).")
    @app_commands.describe(
        nome="Selecione o militar",
        patente="Selecione a patente",
        distintivo="Número ou código do distintivo",
        motivo="Motivo da advertência",
        penalidade="Penalidade aplicada"
    )
    @app_commands.autocomplete(nome=autocomplete_membros, patente=autocomplete_patentes)
    async def advertencia(
        self,
        interaction: discord.Interaction,
        nome: str,
        patente: str,
        distintivo: str,
        motivo: str,
        penalidade: str
    ):
        await interaction.response.defer(ephemeral=True)

        if interaction.user.id != OWNER_ID:
            await interaction.followup.send("❌ Você não tem permissão para usar este comando.", ephemeral=True)
            return

        guild = interaction.guild
        cargo_fixo = guild.get_role(CARGO_FIXO_ID)
        cargo_adv = guild.get_role(CARGO_ADV_ID)
        membro = guild.get_member(int(nome))
        role_patente = guild.get_role(int(patente))
        canal_fixo = guild.get_channel(CANAL_FIXO_ID)

        # Adiciona cargo de advertência ao membro
        if membro and cargo_adv:
            try:
                await membro.add_roles(cargo_adv, reason=f"Advertência registrada por {interaction.user.display_name}")
                # Salva data para remoção automática
                data_remocao = datetime.utcnow() + timedelta(days=DIAS_REMOVER)
                self.advertencias.setdefault(str(guild.id), {})[str(membro.id)] = data_remocao.isoformat()
                self.salvar_dados()
            except discord.Forbidden:
                await interaction.followup.send("❌ Não consegui adicionar o cargo de advertência (permissão insuficiente).", ephemeral=True)
                return
        else:
            await interaction.followup.send("❌ Não foi possível encontrar o membro ou o cargo de advertência.", ephemeral=True)
            return

        # Cria a embed da advertência
        embed = discord.Embed(
            title="📢 Registro de advertência!",
            color=0xFF0000  # Vermelho
        )
        embed.add_field(name="**Nome:**", value=membro.display_name if membro else "Desconhecido", inline=False)
        embed.add_field(name="**Patente:**", value=role_patente.name if role_patente else "Desconhecida", inline=False)
        embed.add_field(name="**Distintivo:**", value=distintivo, inline=False)
        embed.add_field(name="**Motivo:**", value=motivo, inline=False)
        embed.add_field(name="**Consequência:**", value="Advertência Militar", inline=False)
        embed.add_field(name="**Penalidade:**", value=penalidade, inline=False)
        embed.set_footer(text=f"Advertência registrada por {interaction.user.display_name}")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1388215342601605150/1399006385957638214/CDA_-_LOGO_2BPM_Dos_Anjos-1.png")

        if canal_fixo:
            await canal_fixo.send(f"{cargo_fixo.mention}", embed=embed)
            await interaction.followup.send(
                f"✅ Advertência registrada e cargo aplicado! (Será removido em {DIAS_REMOVER} dias)",
                ephemeral=True
            )
        else:
            await interaction.followup.send("❌ Canal fixo não encontrado. Verifique o ID.", ephemeral=True)

    @verificar_remocoes.before_loop
    async def before_verificar_remocoes(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(Advertencia(bot))
