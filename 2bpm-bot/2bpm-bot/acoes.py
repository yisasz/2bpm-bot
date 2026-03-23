import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import json
import os

CANAL_ACAO_ID = 000
CANAL_ESCALACAO_ID = 000
CARGO_MENCAO_ID = 000
MEU_ID = 000

# Caminho do arquivo de bloqueios
CAMINHO_BLOQUEIOS = "bloqueios.json"

if os.path.exists(CAMINHO_BLOQUEIOS):
    with open(CAMINHO_BLOQUEIOS, "r", encoding="utf-8") as f:
        usuarios_bloqueados = json.load(f)
else:
    usuarios_bloqueados = {}

def salvar_bloqueios():
    with open(CAMINHO_BLOQUEIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios_bloqueados, f, ensure_ascii=False, indent=4)

# emojis personalizados de um servidor específico, substitua pelos emojis do seu servidor

def gerar_barra_emojis_custom(atual, total):
    barra = ""
    for i in range(total):
        if i == 0:
            barra += "<:pesq:1395986429347364934>" if atual > 0 else "<:npesq:1395986435231711385>"
        elif i == total - 1:
            barra += "<:pd:1395986431511498802>" if atual > i else "<:npd:1395986438486622318>"
        else:
            barra += "<:vg:1395986427304738858>" if atual > i else "<:nvg:1395986433667240066>"
    return f"`{atual}/{total}`\n{barra}"


class EscalarView(discord.ui.View):
    def __init__(self, bot, acao_id, acoes_ativas, salvar_acoes):
        super().__init__(timeout=None)
        self.bot = bot
        self.acao_id = acao_id
        self.acoes_ativas = acoes_ativas
        self.salvar_acoes = salvar_acoes

    @discord.ui.button(
        label="ᴇsᴄᴀʟᴀʀ",
        style=discord.ButtonStyle.primary,
        emoji="<:blob_police:1395460925212983407>",
        custom_id="botao_escalar"
    )
    async def escalar(self, interaction: discord.Interaction, button: discord.ui.Button):
        usuario = interaction.user

        if self.acao_id not in self.acoes_ativas:
            await interaction.response.send_message("❌ Ação não encontrada ou encerrada.", ephemeral=True)
            return

        # Checar se usuário está bloqueado
        if usuario.display_name in usuarios_bloqueados:
            motivo = usuarios_bloqueados[usuario.display_name]
            await interaction.response.send_message(f"🚫 Você está bloqueado de se candidatar a ações.\nMotivo: {motivo}", ephemeral=True)
            return

        acao = self.acoes_ativas[self.acao_id]

        if usuario.display_name in acao["escalados"]:
            await interaction.response.send_message("⚠️ Você já está escalado para essa ação.", ephemeral=True)
            return

        if len(acao["escalados"]) >= acao["vagas"]:
            await interaction.response.send_message("🚫 Todas as vagas já foram preenchidas.", ephemeral=True)
            return

        acao["escalados"].append(usuario.display_name)
        self.salvar_acoes(self.acoes_ativas)

        escalados_texto = "\n".join(f"- {nome}" for nome in acao["escalados"])
        total_vagas = acao["vagas"]
        total_escalados = len(acao["escalados"])
        barra_progresso = gerar_barra_emojis_custom(total_escalados, total_vagas)

        embed = discord.Embed(
            title="<:32535applicationapprivedids:1395450629521932329> ᴀçãᴏ ᴀɢᴇɴᴅᴀᴅᴀ <:23646yes:1395450614753787985>",
            description=f"**{acao['texto']}**",
            color=discord.Color.green()
        )
        embed.add_field(name="📅  ᴅᴀᴛᴀ", value=f"**`{acao['data']}`**", inline=True)
        embed.add_field(name="⏰  ʜᴏʀáʀɪᴏ", value=f"**`{acao['hora']}`**", inline=True)
        embed.add_field(name="👥  ᴇꜱᴄᴀʟᴀᴅᴏꜱ", value=f"**`{escalados_texto}`**", inline=False)
        embed.add_field(name="<:32040successfulverificationids:1395450624191234179>  ᴠᴀɢᴀs ᴅɪsᴘᴏɴɪᴠᴇɪs", value=barra_progresso, inline=False)

        canal_escalacao = self.bot.get_channel(CANAL_ESCALACAO_ID)
        if canal_escalacao:
            await canal_escalacao.send(embed=embed)

        await interaction.response.send_message(
            f"✅ Você foi escalado com sucesso! Verifique em: {canal_escalacao.mention}", ephemeral=True
        )


class CriarAcaoModal(discord.ui.Modal, title="Criar Nova Ação"):
    def __init__(self, bot, acoes_ativas, salvar_acoes):
        super().__init__()
        self.bot = bot
        self.acoes_ativas = acoes_ativas
        self.salvar_acoes = salvar_acoes

        self.vagas = discord.ui.TextInput(label="Quantidade de vagas", placeholder="Ex: 5", required=True, max_length=3)
        self.texto_acao = discord.ui.TextInput(label="Nome ou descrição da ação", placeholder="Ex: Operação Noturna", required=True, max_length=200)
        self.data = discord.ui.TextInput(label="Data", placeholder="Ex: 20/08/2025", required=True, max_length=10)
        self.hora = discord.ui.TextInput(label="Hora", placeholder="Ex: 21:00", required=True, max_length=5)

        self.add_item(self.vagas)
        self.add_item(self.texto_acao)
        self.add_item(self.data)
        self.add_item(self.hora)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            vagas = int(str(self.vagas))
            if vagas <= 0:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("❌ O campo 'vagas' precisa ser um número positivo.", ephemeral=True)
            return

        try:
            datetime.strptime(str(self.data), "%d/%m/%Y")
        except ValueError:
            await interaction.response.send_message("❌ O campo 'data' precisa estar no formato DD/MM/AAAA e ser válido.", ephemeral=True)
            return

        try:
            datetime.strptime(str(self.hora), "%H:%M")
        except ValueError:
            await interaction.response.send_message("❌ O campo 'hora' precisa estar no formato HH:MM e ser válido.", ephemeral=True)
            return

        acao_id = str(len(self.acoes_ativas) + 1)
        self.acoes_ativas[acao_id] = {
            "vagas": vagas,
            "data": str(self.data),
            "texto": str(self.texto_acao),
            "hora": str(self.hora),
            "escalados": []
        }
        self.salvar_acoes(self.acoes_ativas)

        embed = discord.Embed(
            title="<:42920arrowrightalt:1395450641354063965> **ɴᴏᴠᴀ ᴀᴄ̧ᴀ̃ᴏ ᴅɪꜱᴘᴏɴɪ́ᴠᴇʟ! <:23646yes:1395450614753787985>**",
            description=f"**```{self.texto_acao}```**",
            color=discord.Color.from_rgb(0, 0, 128)
        )
        embed.add_field(name="📅  ᴅᴀᴛᴀ", value=f"**`{self.data}`**", inline=True)
        embed.add_field(name="⏰  ʜᴏʀáʀɪᴏ", value=f"**`{self.hora}`**", inline=True)
        embed.add_field(name="<:86863verifiedmembersids:1395450670261469305>  ᴠᴀɢᴀꜱ", value=f"**`{vagas}`**", inline=False)
        embed.set_footer(text="𝘊𝘭𝘪𝘲𝘶𝘦 𝘯𝘰 𝘣𝘰𝘵ã𝘰 𝘢𝘣𝘢𝘪𝘹𝘰 𝘱𝘢𝘳𝘢 𝘴𝘦 𝘦𝘴𝘤ᴀʟᴀʀ")

        canal_acao = self.bot.get_channel(CANAL_ACAO_ID)
        if canal_acao:
            view = EscalarView(self.bot, acao_id, self.acoes_ativas, self.salvar_acoes)
            await canal_acao.send(content=f"<@&{CARGO_MENCAO_ID}>", embed=embed, view=view)
            await interaction.response.send_message(f"Ação criada com sucesso em {canal_acao.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Canal de ações não encontrado.", ephemeral=True)


class BloquearUsuarioModal(discord.ui.Modal, title="Bloquear Usuário"):
    usuario_input: discord.ui.TextInput

    def __init__(self, usuario):
        super().__init__()
        self.usuario_input = discord.ui.TextInput(label="Motivo do bloqueio", placeholder="Digite o motivo aqui...", required=True, max_length=200)
        self.add_item(self.usuario_input)
        self.usuario = usuario

    async def on_submit(self, interaction: discord.Interaction):
        usuarios_bloqueados[self.usuario.display_name] = str(self.usuario_input)
        salvar_bloqueios()
        await interaction.response.send_message(f"✅ Usuário {self.usuario.display_name} foi bloqueado com sucesso!", ephemeral=True)


class Acoes(commands.Cog):
    def __init__(self, bot, acoes_ativas, salvar_acoes_func):
        self.bot = bot
        self.acoes_ativas = acoes_ativas
        self.salvar_acoes = salvar_acoes_func

    @app_commands.command(name="acao", description="Abrir painel para criar ação")
    async def acao(self, interaction: discord.Interaction):
        if interaction.user.id != MEU_ID:
            await interaction.response.send_message("🚫 Apenas o responsável pelo bot pode criar ações.", ephemeral=True)
            return
        await interaction.response.send_modal(CriarAcaoModal(self.bot, self.acoes_ativas, self.salvar_acoes))

    @app_commands.command(name="bloquearacao", description="Bloquear um usuário de se candidatar a ações")
    @app_commands.describe(usuario="Usuário a ser bloqueado")
    async def bloquearacao(self, interaction: discord.Interaction, usuario: discord.Member):
        await interaction.response.send_modal(BloquearUsuarioModal(usuario))

    @app_commands.command(name="desbloquearacao", description="Desbloquear um usuário de se candidatar a ações")
    @app_commands.describe(usuario="Usuário a ser desbloqueado")
    async def desbloquearacao(self, interaction: discord.Interaction, usuario: discord.Member):
        if usuario.display_name in usuarios_bloqueados:
            usuarios_bloqueados.pop(usuario.display_name)
            salvar_bloqueios()
            await interaction.response.send_message(f"✅ Usuário {usuario.display_name} agora poderá se candidatar a ações.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ Usuário {usuario.display_name} não estava bloqueado.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Acoes(bot, {}, lambda x: None))
