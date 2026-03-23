import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta


class AdvDiscord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # trocar pelos ids reais do seu servidor
        self.CARGO_SUPERVISOR = 000
        self.CARGO_ADV1 = 000
        self.CARGO_ADV2 = 000
        self.CARGO_POLICIA = 000
        self.CANAL_ADV = 000


    @app_commands.command(name="advdiscord", description="Aplicar advertência")
    @app_commands.choices(nivel=[
        app_commands.Choice(name="ADV 01", value=1),
        app_commands.Choice(name="ADV 02", value=2),
        app_commands.Choice(name="ADV 03", value=3),
    ])
    async def advdiscord(
        self,
        interaction: discord.Interaction,
        nivel: app_commands.Choice[int],
        usuario: discord.Member,
        motivo: str
    ):

        await interaction.response.defer(ephemeral=True)

        # permissão
        if not any(role.id == self.CARGO_SUPERVISOR for role in interaction.user.roles):
            return await interaction.followup.send("Você não possui permissão.")

        guild = interaction.guild
        canal = guild.get_channel(self.CANAL_ADV)

        if not canal:
            return await interaction.followup.send(
                "Canal de advertências não encontrado."
            )

        cargo_adv1 = guild.get_role(self.CARGO_ADV1)
        cargo_adv2 = guild.get_role(self.CARGO_ADV2)
        cargo_policia = guild.get_role(self.CARGO_POLICIA)

        # proteções importantes
        if usuario == interaction.user:
            return await interaction.followup.send(
                "Você não pode aplicar advertência em si mesma."
            )

        if usuario == guild.owner:
            return await interaction.followup.send(
                "Você não pode advertir o dono do servidor."
            )

        if usuario.top_role >= interaction.user.top_role:
            return await interaction.followup.send(
                "Você não pode advertir alguém com cargo igual ou superior."
            )

        try:

            # ADV 01
            if nivel.value == 1:
                if cargo_adv1:
                    await usuario.add_roles(cargo_adv1)

                acao = "Recebeu ADV 01"
                marcar_cargo = True 

            # ADV 02
            elif nivel.value == 2:
                if cargo_adv2:
                    await usuario.add_roles(cargo_adv2)

                await usuario.timeout(timedelta(hours=24))

                acao = "Recebeu ADV 02 + Timeout de 24h"
                marcar_cargo = True


            # ADV 03
            else:
                acao = "ADV 03 — Resolver em ticket com a Staff"
                marcar_cargo = True

        except discord.Forbidden:
            return await interaction.followup.send(
                "Não tenho permissão para gerenciar esse usuário."
            )

        # Embed 
        embed = discord.Embed(
            title="🚨 Advertência Registrada",
            color=discord.Color.dark_red()
        )

        embed.add_field(name="Usuário", value=usuario.mention, inline=False)
        embed.add_field(name="Ação", value=acao, inline=False)
        embed.add_field(name="Supervisor", value=interaction.user.mention, inline=False)
        embed.add_field(name="Motivo", value=f"```{motivo}```", inline=False)

        embed.set_footer(text="Sistema interno de moderação")
        embed.timestamp = discord.utils.utcnow()

        # marcar cargo de todos do servidor
        if marcar_cargo and cargo_policia:
            content = f"🚨 Atenção {cargo_policia.mention}"
        else:
            content = None

        await canal.send(
            content=content,
            embed=embed,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

        await interaction.followup.send(
            f"✅ Advertência aplicada com sucesso em {usuario.mention}."
        )


async def setup(bot):
    await bot.add_cog(AdvDiscord(bot))
