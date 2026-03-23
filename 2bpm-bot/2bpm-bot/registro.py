import discord
from discord.ext import commands, tasks
import json

CAMINHO_USUARIOS = "usuarios.json"
ID_CANAL_REGISTRO = 000  # Canal que o usuario ira solicitar set
usuarios = {}


def salvar_em_arquivo(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


class FormularioRegistro(discord.ui.Modal, title="Registro de Identidade"):
    nome = discord.ui.TextInput(label="Nome", placeholder="Digite seu nome")
    sobrenome = discord.ui.TextInput(
        label="Sobrenome", placeholder="Digite seu sobrenome"
    )
    passaporte = discord.ui.TextInput(
        label="Passaporte", placeholder="Digite seu número de passaporte"
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        novo_nick = (
            f"{self.nome.value} {self.sobrenome.value} | {self.passaporte.value}"
        )
        try:
            await interaction.user.edit(nick=novo_nick)

            usuarios[str(interaction.user.id)] = {
                "nome": self.nome.value,
                "sobrenome": self.sobrenome.value,
                "passaporte": self.passaporte.value,
            }
            salvar_em_arquivo(CAMINHO_USUARIOS, usuarios)

            role_policia = discord.utils.get(
                interaction.guild.roles, name="🚨・Policia"
            )
            role_aluno = discord.utils.get(interaction.guild.roles, name="👮🏻‍♂️・Aluno")
            role_visitante = discord.utils.get(
                interaction.guild.roles, name="visitante"
            )

            mensagens = []

            # Remove visitante antes
            if role_visitante and role_visitante in interaction.user.roles:
                await interaction.user.remove_roles(role_visitante)
                mensagens.append("❌ Removido: visitante")

            # Adiciona aluno
            if role_aluno:
                await interaction.user.add_roles(role_aluno)
                mensagens.append("👮🏻‍♂️・Aluno")

            # Adiciona polícia
            if role_policia:
                await interaction.user.add_roles(role_policia)
                mensagens.append("🚨・Policia")

            # Mensagem final
            embed_final = discord.Embed(
                title="**REGISTRO COMPLETO!**",
                description="*Seja bem-vindo(a) ao 2º BPM!*",
                color=8251020,
            )
            embed_final.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            embed_final.add_field(
                name="👤 Nome alterado para:", value=novo_nick, inline=True
            )
            embed_final.add_field(
                name="🛂 Passaporte:", value=self.passaporte.value, inline=False
            )

            await interaction.response.send_message(embed=embed_final, ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Não consegui mudar seu nome ou atribuir cargos. Verifique minhas permissões.",
                ephemeral=True,
            )


class BotaoRegistro(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Iniciar Registro",
        style=discord.ButtonStyle.green,
        custom_id="botao_registro",
    )
    async def iniciar_registro(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        modal = FormularioRegistro(self.bot)
        await interaction.response.send_modal(modal)


class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enviar_mensagem_inicial.start()

    @tasks.loop(count=1)
    async def enviar_mensagem_inicial(self):
        await self.bot.wait_until_ready()
        canal = self.bot.get_channel(ID_CANAL_REGISTRO)
        if canal:
            async for msg in canal.history(limit=10):
                if msg.author == self.bot.user and msg.components:
                    return
            view = BotaoRegistro(self.bot)
            embed = discord.Embed(
                title="🔰 Registro de Identidade",
                description="Clique no botão abaixo para iniciar seu registro no batalhão.",
                color=discord.Color.blurple(),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )

            await canal.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Registro(bot))
