import discord
from discord.ext import commands
from discord import app_commands


class PrenderList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="prenderlist", description="Veja a lista de itens apreensíveis."
    )
    async def prenderlist(self, interaction: discord.Interaction):
        itens_apreensiveis = [
            "Algema",
            "Barreira",
            "Capuz",
            "Carreira de Cocaina",
            "Cartão de acesso R",
            "Cartão Ilegível",
            "Cassete",
            "Cigarro de Maconha",
            "Circuito Eletrônico",
            "Clonagem de Cocaina",
            "Clonagem de Maconha",
            "Colete",
            "Corpo de Pistola",
            "Corpo de Rifle",
            "Corpo de Sub",
            "Empunhadura",
            "Energético",
            "Explosivo",
            "Folha de Cocaina",
            "Folha de Maconha",
            "Gazua",
            "Gazua++",
            "Kit Químico",
            "Kit Residual",
            "Lanterna Tática",
            "Mesa de Produção",
            "Metanfetamina",
            "Mira Holográfica",
            "Munições",
            "Pacote de Cannabis",
            "Pacote de Cocaina",
            "Pacote de Metanfetamina",
            "Pager",
            "Peças de arma",
            "Pente Estendido",
            "Placa de colete",
            "Placa de trânsito",
            "Placa Veicular",
            "Silenciador",
            "Spike",
            "Tablet Descartável",
            "Taser",
            "Celular",
            "Radio",
            "Bastão de Beisebol",
            "Canivete",
            "Corda",
            "Facão",
            "Isqueiro",
            "Lanterna",
            "Machado",
            "Machado de Batalha",
            "Machado de Pedra",
            "Maleta",
            "Pé de cabra",
            "Roupa de Mergulho",
            "Soco inglês",
            "Taco de Golfe",
            "Taco de Sinuca",
            "Platina",
            "Bateria AA",
            "Bateria AAA",
            "Cabo de Alimentação",
            "Chapa de Metal",
            "Chave 01",
            "Chave 02",
            "Colar de Ouro",
            "Colar de Prata",
            "Componente Eletrônico",
            "Dinheiro Molhado",
            "Dinheiro Sujo",
            "Estatueta de Cavalo",
            "Fita adesiva",
            "Fita isolante",
            "Fonte de alimentação",
            "Frasco de pólvora",
            "Leão de Ouro",
            "Leopardo de Ouro",
            "Lona",
            "Martelo",
            "Memória Ram",
            "Nota Promissória",
            "Parafusos",
            "Pasta de dente",
            "Pendriver seguro",
            "Placa de vídeo",
            "Porcas de Parafuso",
            "Processador",
            "Televisão",
            "Unidade SSD",
            "Ventoinha de processador",
            "Sucata de metal",
            "ecu",
        ]

        lista = "\n".join(f"🔸 {item}" for item in itens_apreensiveis)

        embed = discord.Embed(
            title="📋 Lista de Itens Apreensíveis", description=lista, color=0x005CCF
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(PrenderList(bot))
