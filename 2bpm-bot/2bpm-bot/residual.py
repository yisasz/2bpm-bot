import discord
from discord import app_commands
from discord.ext import commands


class ResidualView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Mapeamento QRU -> Residual
        self.residuais = {
            "QRU de Disparo": "Pólvora",
            "QRU de ATM": "Linter",
            "QRU de registradora": "Linter",
            "QRU de Tráfico de drogas": "Narcóticos/Drogas",
            "QRU de Roubo a Porta Malas": "Ferro",
            "QRU de Roubo de Veículos": "Alumínio",
            "QRU de Roubo de Pertences": "Clorofórmio",
            "QRU de Lavagem de Dinheiro": "Linter",
            "QRU de roubo a Propriedade": "Alumínio",
            "QRU de roubo a Carro Forte": "Ferro",
        }

        # Cria o select menu com emojis
        options = [
            discord.SelectOption(label="QRU de Disparo", emoji="🔫"),
            discord.SelectOption(label="QRU de ATM", emoji="🏧"),
            discord.SelectOption(label="QRU de registradora", emoji="💵"),
            discord.SelectOption(label="QRU de Tráfico de drogas", emoji="💊"),
            discord.SelectOption(label="QRU de Roubo a Porta Malas", emoji="🧳"),
            discord.SelectOption(label="QRU de Roubo de Veículos", emoji="🚗"),
            discord.SelectOption(label="QRU de Roubo de Pertences", emoji="🎒"),
            discord.SelectOption(label="QRU de Lavagem de Dinheiro", emoji="💸"),
            discord.SelectOption(label="QRU de roubo a Propriedade", emoji="��"),
            discord.SelectOption(label="QRU de roubo a Carro Forte", emoji="🚙"),
        ]
        self.add_item(ResidualSelect(options, self.residuais))


class ResidualSelect(discord.ui.Select):
    def __init__(self, options, residuais):
        super().__init__(
            placeholder="Selecione uma QRU...",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.residuais = residuais

    async def callback(self, interaction: discord.Interaction):
        try:
            qru = self.values[0]
            residual = self.residuais[qru]

            embed = discord.Embed(
                title="🔎 Consulta de Residual",
                description=f"**{qru}** corresponde ao residual:\n```yaml\n{residual}\n```",
                color=discord.Color.dark_blue(),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png"
            )

            await interaction.response.edit_message(embed=embed, view=self.view)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Ocorreu um erro ao processar: `{e}`", ephemeral=True
            )


class Residual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="residual", description="Consulta os resíduos correspondentes a uma QRU."
    )
    async def residual(self, interaction: discord.Interaction):
        try:
            # Garante que o Discord saiba que o bot vai responder
            await interaction.response.defer(ephemeral=False)

            view = ResidualView()
            embed = discord.Embed(
                title="🔎 Consulta de Residual",
                description="Selecione uma das QRUs no menu abaixo para consultar o residual correspondente.",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png"
            )

            # Usa followup porque já foi feito o defer
            await interaction.followup.send(embed=embed, view=view, ephemeral=False)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erro ao executar o comando: `{e}`", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Residual(bot))
