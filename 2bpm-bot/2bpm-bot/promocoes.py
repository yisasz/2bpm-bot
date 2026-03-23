import discord
from discord.ext import commands
from discord import app_commands

CANAL_PROMOCOES_ID = 000
USUARIOS_AUTORIZADOS = [
    000,
    000,
]  # IDs dos usuários autorizados a usar os comandos de promoção

CARGOS_MILITARES = [
    "👮🏻‍♂️・Aluno",
    "👮🏻‍♂️・Soldado",
    "👮🏻‍♂️・Cabo",
    "👮🏻‍♂️・3 Sargento",
    "👮🏻‍♂️・2 Sargento",
    "👮🏻‍♂️・1 Sargento",
    "👮🏻‍♂️・Sub Tenente",
    "👮🏻‍♂️・Aspirante a Tenente",
    "👮🏻‍♂️・2 Tenente",
    "👮🏻‍♂️・1 Tenente",
    "👮🏻‍♂️・Capitão",
    "👮🏻‍♂️・Major",
    "👮🏻‍♂️・Tentente Coronel",
    "👮🏻‍♂️・Coronel",
]


class Promocoes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Função de autocomplete genérica para cargos do servidor
    async def autocomplete_cargos(self, interaction: discord.Interaction, current: str):
        cargos = [
            role.name for role in interaction.guild.roles if not role.is_default()
        ]
        resultados = [c for c in cargos if current.lower() in c.lower()]
        return [app_commands.Choice(name=c, value=c) for c in resultados[:25]]

    @app_commands.command(name="promover", description="Registra uma promoção oficial")
    @app_commands.describe(
        membro="Quem foi promovido",
        novo_cargo="Novo cargo da pessoa (exatamente como está no Discord)",
        motivo="Motivo ou mérito da promoção",
    )
    @app_commands.autocomplete(novo_cargo=autocomplete_cargos)
    async def promover(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        novo_cargo: str,
        motivo: str,
    ):
        if interaction.user.id not in USUARIOS_AUTORIZADOS:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.", ephemeral=True
            )
            return
        await self.processar_promocao(interaction, membro, novo_cargo, motivo)

    # Comando lote: todos os novo_cargoX recebem o mesmo autocomplete
    @app_commands.command(
        name="promover_lote", description="Faz até 8 promoções de uma vez"
    )
    @app_commands.describe(
        membro1="Primeiro membro a promover",
        novo_cargo1="Cargo 1",
        motivo1="Motivo 1",
        membro2="Segundo membro a promover",
        novo_cargo2="Cargo 2",
        motivo2="Motivo 2",
        membro3="Terceiro membro a promover",
        novo_cargo3="Cargo 3",
        motivo3="Motivo 3",
        membro4="Quarto membro a promover",
        novo_cargo4="Cargo 4",
        motivo4="Motivo 4",
        membro5="Quinto membro a promover",
        novo_cargo5="Cargo 5",
        motivo5="Motivo 5",
        membro6="Sexto membro a promover",
        novo_cargo6="Cargo 6",
        motivo6="Motivo 6",
        membro7="Sétimo membro a promover",
        novo_cargo7="Cargo 7",
        motivo7="Motivo 7",
        membro8="Oitavo membro a promover",
        novo_cargo8="Cargo 8",
        motivo8="Motivo 8",
    )
    @app_commands.autocomplete(novo_cargo1=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo2=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo3=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo4=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo5=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo6=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo7=autocomplete_cargos)
    @app_commands.autocomplete(novo_cargo8=autocomplete_cargos)
    async def promover_lote(
        self,
        interaction: discord.Interaction,
        membro1: discord.Member,
        novo_cargo1: str,
        motivo1: str,
        membro2: discord.Member = None,
        novo_cargo2: str = None,
        motivo2: str = None,
        membro3: discord.Member = None,
        novo_cargo3: str = None,
        motivo3: str = None,
        membro4: discord.Member = None,
        novo_cargo4: str = None,
        motivo4: str = None,
        membro5: discord.Member = None,
        novo_cargo5: str = None,
        motivo5: str = None,
        membro6: discord.Member = None,
        novo_cargo6: str = None,
        motivo6: str = None,
        membro7: discord.Member = None,
        novo_cargo7: str = None,
        motivo7: str = None,
        membro8: discord.Member = None,
        novo_cargo8: str = None,
        motivo8: str = None,
    ):
        if interaction.user.id not in USUARIOS_AUTORIZADOS:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)
        canal = interaction.guild.get_channel(CANAL_PROMOCOES_ID)

        promocoes = [
            (membro1, novo_cargo1, motivo1),
            (membro2, novo_cargo2, motivo2),
            (membro3, novo_cargo3, motivo3),
            (membro4, novo_cargo4, motivo4),
            (membro5, novo_cargo5, motivo5),
            (membro6, novo_cargo6, motivo6),
            (membro7, novo_cargo7, motivo7),
            (membro8, novo_cargo8, motivo8),
        ]

        total_sucesso, total_falha = 0, 0

        for membro, novo_cargo, motivo in promocoes:
            if not membro or not novo_cargo or not motivo:
                continue
            try:
                await self.processar_promocao(
                    interaction,
                    membro,
                    novo_cargo,
                    motivo,
                    canal=canal,
                    enviar_resposta=False,
                )
                total_sucesso += 1
            except Exception as e:
                total_falha += 1
                print(f"Erro ao promover {membro}: {e}")

        await interaction.followup.send(
            f"✅ Promoções processadas. Sucesso: {total_sucesso}, Falhas: {total_falha}.",
            ephemeral=True,
        )

    async def processar_promocao(
        self, interaction, membro, novo_cargo, motivo, canal=None, enviar_resposta=True
    ):
        canal = canal or interaction.guild.get_channel(CANAL_PROMOCOES_ID)
        cargo_encontrado = discord.utils.get(interaction.guild.roles, name=novo_cargo)

        if not cargo_encontrado:
            if enviar_resposta:
                await interaction.response.send_message(
                    f"❌ Cargo '{novo_cargo}' não encontrado.", ephemeral=True
                )
            raise ValueError(f"Cargo '{novo_cargo}' não encontrado")

        try:
            # Remove cargos militares antigos, exceto o novo
            for cargo in membro.roles:
                if cargo.name in CARGOS_MILITARES and cargo.name != novo_cargo:
                    await membro.remove_roles(cargo)
            await membro.add_roles(cargo_encontrado)
        except discord.Forbidden:
            if enviar_resposta:
                await interaction.response.send_message(
                    "❌ Permissão insuficiente para aplicar o cargo.", ephemeral=True
                )
            raise

        embed = discord.Embed(
            title="📢 PROMOÇÃO OFICIAL!",
            description=f"{membro.mention} foi promovido a **{novo_cargo}**!",
            color=0x005CFF,
        )
        embed.add_field(name="🎖️ Motivo", value=motivo, inline=False)
        embed.set_footer(text=f"Promoção feita por {interaction.user.display_name}")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1388215342601605150/1399006385957638214/CDA_-_LOGO_2BPM_Dos_Anjos-1.png"
        )

        await canal.send(embed=embed)

        # Tenta mandar DM para o promovido
        try:
            dm_embed = discord.Embed(
                title="🎉 Parabéns pela promoção!",
                description=f"Você foi promovido a **{novo_cargo}** no servidor {interaction.guild.name}.\n\nMotivo: {motivo}",
                color=0x00FF00,
            )
            dm_embed.set_footer(
                text=f"Promoção feita por {interaction.user.display_name}"
            )
            dm_embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1388215342601605150/1399006385957638214/CDA_-_LOGO_2BPM_Dos_Anjos-1.png"
            )
            await membro.send(embed=dm_embed)
        except discord.Forbidden:
            pass

        if enviar_resposta:
            await interaction.response.send_message(
                "✅ Promoção registrada com sucesso e DM enviada!", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Promocoes(bot))
