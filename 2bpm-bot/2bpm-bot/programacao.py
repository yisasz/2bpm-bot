import discord
from discord.ext import commands
import json
import os

# ===== CONFIGURAÇÕES =====

USUARIO_AUTORIZADO_ID = 000

CANAL_COMANDO_ID = 000
CANAL_EMBED_ID = 000
CARGO_MENCAO_ID = 000
ARQUIVO_EVENTOS = "eventos_programacao.json"


# ===== JSON =====


def carregar_eventos():
    if os.path.exists(ARQUIVO_EVENTOS):
        with open(ARQUIVO_EVENTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_eventos(eventos):
    with open(ARQUIVO_EVENTOS, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)


# ===== EMBED =====


def gerar_embed():

    eventos = carregar_eventos()

    embed = discord.Embed(
        title="📅 Programação", description="Eventos programados:", color=0x2B2D31
    )

    semanais = []
    mensais = []

    for e in eventos:

        texto = f"📆 {e['data']}\n📝 {e['descricao']}"

        if e["tipo"] == "Semanal":
            semanais.append(f"**{e['nome']}**\n{texto}")

        else:
            mensais.append(f"**{e['nome']}**\n{texto}")

    if semanais:
        embed.add_field(
            name="📆 Eventos Semanais", value="\n\n".join(semanais), inline=False
        )

    if mensais:
        embed.add_field(
            name="📅 Eventos Mensais", value="\n\n".join(mensais), inline=False
        )

    if not eventos:
        embed.description = "Nenhum evento cadastrado."

    embed.set_footer(text="Sistema de programação")

    return embed


# ===== MODAL =====


class AgendarModal(discord.ui.Modal, title="Agendar Evento"):

    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo

    nome = discord.ui.TextInput(label="Nome do evento")

    data = discord.ui.TextInput(label="Data ou dia da semana")

    descricao = discord.ui.TextInput(
        label="Descrição", style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):

        eventos = carregar_eventos()

        eventos.append(
            {
                "nome": self.nome.value,
                "data": self.data.value,
                "descricao": self.descricao.value,
                "tipo": self.tipo,
            }
        )

        salvar_eventos(eventos)

        canal = interaction.client.get_channel(CANAL_EMBED_ID)

        embed = gerar_embed()

        async for msg in canal.history(limit=10):
            if msg.author == interaction.client.user and msg.embeds:
                await msg.edit(embed=embed, view=ProgramacaoView(interaction.client))
                break

        await interaction.response.send_message("✅ Evento adicionado.", ephemeral=True)


# ===== ESCOLHER TIPO =====


class EscolherTipoView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Escolha o tipo do evento",
        options=[
            discord.SelectOption(label="Semanal", emoji="📆"),
            discord.SelectOption(label="Mensal", emoji="📅"),
        ],
    )
    async def selecionar(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):

        tipo = select.values[0]

        await interaction.response.send_modal(AgendarModal(tipo))


# ===== REMOVER EVENTO =====


class RemoverView(discord.ui.View):

    def __init__(self, bot, eventos):

        super().__init__(timeout=60)

        self.bot = bot
        self.eventos = eventos

        options = []

        for i, e in enumerate(eventos):

            options.append(
                discord.SelectOption(
                    label=e["nome"],
                    description=f"{e['tipo']} • {e['data']}",
                    value=str(i),
                )
            )

        select = discord.ui.Select(
            placeholder="Escolha um evento para remover", options=options
        )

        select.callback = self.remover_evento

        self.add_item(select)

    async def remover_evento(self, interaction: discord.Interaction):

        index = int(interaction.data["values"][0])

        self.eventos.pop(index)

        salvar_eventos(self.eventos)

        canal = interaction.client.get_channel(CANAL_EMBED_ID)

        embed = gerar_embed()

        async for msg in canal.history(limit=10):
            if msg.author == interaction.client.user and msg.embeds:
                await msg.edit(embed=embed, view=ProgramacaoView(self.bot))
                break

        await interaction.response.send_message("🗑 Evento removido.", ephemeral=True)


# ===== VIEW =====


class ProgramacaoView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction):

        if interaction.user.id != USUARIO_AUTORIZADO_ID:

            await interaction.response.send_message(
                "❌ Você não tem permissão.", ephemeral=True
            )

            return False

        return True

    @discord.ui.button(
        label="Agendar",
        style=discord.ButtonStyle.green,
        emoji="📅",
        custom_id="agendar_evento_programacao",
    )
    async def agendar(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):

        view = EscolherTipoView()

        await interaction.response.send_message(
            "Escolha o tipo do evento:", view=view, ephemeral=True
        )

    @discord.ui.button(
        label="Gerenciar",
        style=discord.ButtonStyle.blurple,
        emoji="⚙️",
        custom_id="gerenciar_eventos_programacao",
    )
    async def gerenciar(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):

        eventos = carregar_eventos()

        if not eventos:

            await interaction.response.send_message(
                "❌ Nenhum evento cadastrado.", ephemeral=True
            )

            return

        view = RemoverView(self.bot, eventos)

        embed = discord.Embed(
            title="Gerenciar Eventos",
            description="Selecione um evento para remover.",
            color=0xFFCC00,
        )

        for i, e in enumerate(eventos):

            embed.add_field(
                name=f"{i+1} - {e['nome']}",
                value=f"{e['tipo']} • {e['data']}",
                inline=False,
            )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# ===== COG =====


class Programacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def programacao(self, ctx):

        if ctx.author.id != USUARIO_AUTORIZADO_ID:
            return

        if ctx.channel.id != CANAL_COMANDO_ID:
            return

        canal = self.bot.get_channel(CANAL_EMBED_ID)

        embed = gerar_embed()

        await canal.send(
            f"<@&{CARGO_MENCAO_ID}>", embed=embed, view=ProgramacaoView(self.bot)
        )

        await ctx.send("✅ Programação enviada.", delete_after=5)


# ===== SETUP =====


async def setup(bot):

    await bot.add_cog(Programacao(bot))

    bot.add_view(ProgramacaoView(bot))
