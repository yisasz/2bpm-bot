import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import json
import os
from typing import Optional

CAMINHO_LIVES = "lives_registradas.json"
OWNER_ID = 000
CANAL_LIVES_ID = 000
CANAL_SET_LIVES = 000


# ======= FUNÇÕES DE ARQUIVO =======


def carregar_arquivo(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def salvar_em_arquivo(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# inicializa a variável global (pode ser recarregada quando necessário)
lives_registradas = carregar_arquivo(CAMINHO_LIVES)


# ======= COG DE LIVES =======


class EditLiveModal(discord.ui.Modal):
    def __init__(self, old_name: str, old_link: str):
        super().__init__(title="Editar Live")

        self.old_name = old_name

        self.novo_nome = discord.ui.TextInput(
            label="Novo nome da live",
            style=discord.TextStyle.short,
            default=old_name,
            max_length=100,
            required=True,
        )
        self.add_item(self.novo_nome)

        self.novo_link = discord.ui.TextInput(
            label="Novo link da live",
            style=discord.TextStyle.short,
            default=old_link,
            max_length=200,
            required=True,
        )
        self.add_item(self.novo_link)

    async def on_submit(self, interaction: discord.Interaction):
        novo_nome = self.novo_nome.value.strip()
        novo_link = self.novo_link.value.strip()

        dados = carregar_arquivo(CAMINHO_LIVES)

        if self.old_name not in dados:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Live não encontrada",
                    description="A live selecionada não existe mais no registro.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        autor = dados[self.old_name].get("autor", "")

        if autor != interaction.user.display_name and interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Permissão negada",
                    description="Você não pode editar esta live.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        if novo_nome != self.old_name and novo_nome in dados:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Nome já existe",
                    description="Já existe outra live com esse nome.",
                    color=discord.Color.orange(),
                ),
                ephemeral=True,
            )
            return

        registro = dados.pop(self.old_name)
        registro["link"] = novo_link
        dados[novo_nome] = registro

        salvar_em_arquivo(CAMINHO_LIVES, dados)

        embed = discord.Embed(title="Live atualizada", color=discord.Color.green())
        embed.add_field(name="Nome", value=novo_nome, inline=False)
        embed.add_field(name="Link", value=novo_link, inline=False)
        embed.set_footer(text="Alteração registrada com sucesso.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class LiveSelect(discord.ui.Select):
    def __init__(self, options, bot):
        super().__init__(
            placeholder="Selecione a live que deseja editar...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="editar_live_select",  # bom para persistência futura
        )
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        # Recarrega dados atualizados
        dados = carregar_arquivo(CAMINHO_LIVES)

        escolha = self.values[0]  # nome da live (usamos o nome como value)

        if escolha not in dados:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Live não encontrada",
                    description="A live selecionada não está mais disponível.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        autor = dados[escolha].get("autor", "")
        if autor != interaction.user.display_name and interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Permissão negada",
                    description="Você não tem permissão para editar esta live.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        old_link = dados[escolha].get("link", "")
        modal = EditLiveModal(old_name=escolha, old_link=old_link)
        # envia o modal direto como resposta à interação do select
        await interaction.response.send_modal(modal)


class LiveSelectView(discord.ui.View):
    def __init__(self, options, bot, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.add_item(LiveSelect(options=options, bot=bot))


class Lives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="registrolive", description="Registra uma nova live no sistema."
    )
    async def registrolive(self, interaction: discord.Interaction):
        if interaction.channel.id != CANAL_SET_LIVES:
            embed = discord.Embed(
                title="Acesso negado",
                description="Você deve usar este comando no canal autorizado para registro de lives.",
                color=discord.Color.red(),
            )
            embed.set_footer(text="Verifique o canal e tente novamente.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed_nome = discord.Embed(
            title="Registro de live",
            description="Digite abaixo o nome da live que deseja registrar.",
            color=discord.Colour.blue(),
        )
        embed_nome.set_footer(text="Etapa 1 de 2 • Nome da live")
        embed_nome.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/2989/2989988.png"
        )
        await interaction.response.send_message(embed=embed_nome, ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg_nome = await self.bot.wait_for("message", timeout=30.0, check=check)
            nome_live = msg_nome.content.strip()

            # atualiza lista local antes de validar
            dados_atual = carregar_arquivo(CAMINHO_LIVES)

            if nome_live in dados_atual:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Live já registrada",
                        description="Essa live já foi registrada anteriormente no sistema.",
                        color=discord.Color.orange(),
                    ),
                    ephemeral=True,
                )
                return

            await interaction.followup.send(
                "Agora digite o link da live:", ephemeral=True
            )
            msg_link = await self.bot.wait_for("message", timeout=30.0, check=check)
            link_live = msg_link.content.strip()

            # garantir que carregamos a versão atual antes de salvar
            dados_atual = carregar_arquivo(CAMINHO_LIVES)

            dados_atual[nome_live] = {
                "autor": interaction.user.display_name,
                "link": link_live,
            }

            salvar_em_arquivo(CAMINHO_LIVES, dados_atual)

            embed = discord.Embed(
                title="Live registrada com sucesso", color=discord.Color.green()
            )
            embed.add_field(name="Nome da live", value=nome_live, inline=False)
            embed.add_field(name="Link da live", value=link_live, inline=False)
            embed.set_footer(text="Registro finalizado com êxito.")
            await interaction.followup.send(embed=embed)

        except asyncio.TimeoutError:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Tempo esgotado",
                    description="Você demorou demais para responder. Refaça o processo usando o comando novamente.",
                    color=discord.Color.orange(),
                ),
                ephemeral=True,
            )

    @app_commands.command(name="excluirlive", description="Exclui uma live registrada.")
    async def excluirlive(self, interaction: discord.Interaction):
        if interaction.channel.id != CANAL_SET_LIVES:
            await interaction.response.send_message(
                "Use este comando apenas no canal correto.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Digite o nome da live que deseja excluir:", ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            nome_live = msg.content.strip()

            dados_atual = carregar_arquivo(CAMINHO_LIVES)
            autor_live = dados_atual.get(nome_live, {}).get("autor", "")
            if nome_live in dados_atual and (
                autor_live == interaction.user.display_name
                or interaction.user.id == OWNER_ID
            ):
                del dados_atual[nome_live]
                salvar_em_arquivo(CAMINHO_LIVES, dados_atual)
                embed = discord.Embed(
                    title="Live excluída",
                    description=f"A live {nome_live} foi removida com sucesso.",
                    color=discord.Color.red(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Ação negada",
                        description="Live não encontrada ou você não tem permissão para excluí-la.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        except asyncio.TimeoutError:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Tempo esgotado",
                    description="Você demorou demais para responder. Refaça o processo usando o comando novamente.",
                    color=discord.Color.orange(),
                ),
                ephemeral=True,
            )

    @app_commands.command(
        name="editarlive", description="Edita nome e link de uma live."
    )
    async def editarlive(self, interaction: discord.Interaction):
        # Verifica canal
        if interaction.channel.id != CANAL_SET_LIVES:
            await interaction.response.send_message(
                "Use este comando apenas no canal correto.", ephemeral=True
            )
            return

        # Recarrega as lives do arquivo para garantir versão atual
        dados = carregar_arquivo(CAMINHO_LIVES)

        if not dados:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Nenhuma live registrada",
                    description="Não há lives registradas no sistema.",
                    color=discord.Color.dark_gray(),
                ),
                ephemeral=True,
            )
            return

        # Cria opções para o select (até 25 por limitação do Discord)
        options = []
        count = 0
        for nome, info in dados.items():
            if count >= 25:
                break
            # descrição curta com link truncado (ou autor)
            link_preview = info.get("link", "")
            if len(link_preview) > 80:
                link_preview = link_preview[:77] + "..."
            desc = (
                f"{info.get('autor','')} • {link_preview}"
                if info.get("autor")
                else link_preview
            )
            options.append(
                discord.SelectOption(label=nome, value=nome, description=desc[:100])
            )
            count += 1

        # Usar timeout=None para evitar expiração rápida — o usuário terá tempo para interagir
        view = LiveSelectView(options=options, bot=self.bot, timeout=None)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Editar live",
                description="Selecione a live que deseja editar no menu abaixo. Após selecionar, preencha o formulário com o novo nome e o novo link.",
                color=discord.Color.blue(),
            ),
            view=view,
            ephemeral=True,
        )


# ======= TWITCH & YOUTUBE =======


async def get_twitch_app_token(client_id, client_secret):
    url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            data = await resp.json()
            return data.get("access_token")


def extrair_canal_twitch(link):
    partes = link.split("twitch.tv/")
    return partes[1].split("/")[0] if len(partes) > 1 else None


async def verificar_live_twitch(session, token, client_id, canal):
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    url = f"https://api.twitch.tv/helix/streams?user_login={canal}"
    async with session.get(url, headers=headers) as resp:
        data = await resp.json()
        return bool(data.get("data"))


async def verificar_live_youtube(session, link):
    try:
        async with session.get(link) as resp:
            html = await resp.text()
            return "isLiveNow" in html or "LIVE_NOW" in html
    except Exception as e:
        print(f"Erro ao verificar live YouTube: {e}")
        return False


# ======= ATUALIZAÇÃO AUTOMÁTICA =======


@tasks.loop(seconds=180)
async def atualizar_lives():
    bot = atualizar_lives.bot_reference

    try:
        canal = await bot.fetch_channel(CANAL_LIVES_ID)
    except discord.NotFound:
        print("Canal de lives não encontrado.")
        return

    ordem_patentes = {
        "Coronel": 1,
        "Tenente Coronel": 2,
        "Major": 3,
        "Capitão": 4,
        "1 Tenente": 5,
        "2 Tenente": 6,
        "Aspirante a Tenente": 7,
        "Sub Tenente": 8,
        "1 Sargento": 9,
        "1 SGT": 9,
        "2 Sargento": 10,
        "2 SGT": 10,
        "3 Sargento": 11,
        "3 SGT": 11,
        "Cabo": 12,
        "Soldado": 13,
        "1SD": 13,
        "Aluno": 14,
        "Aluna": 14,
        "2SD": 14,
    }

    def get_ordem_por_patente(nome):
        for patente, ordem in ordem_patentes.items():
            if patente.lower() in nome.lower():
                return ordem
        return 99

    # substitua pelos seus próprios IDs e token
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    lives_ativas = []

    async with aiohttp.ClientSession() as session:
        access_token = await get_twitch_app_token(CLIENT_ID, CLIENT_SECRET)
        # recarrega do arquivo para manter dados atualizados
        dados_atuais = carregar_arquivo(CAMINHO_LIVES)
        lives_ordenadas = sorted(
            dados_atuais.items(), key=lambda item: get_ordem_por_patente(item[0])
        )

        for nome, dados in lives_ordenadas:
            link = dados.get("link", "").strip()
            if not link:
                continue

            online = False

            if "twitch.tv" in link:
                canal_twitch = extrair_canal_twitch(link)
                if canal_twitch:
                    try:
                        online = await verificar_live_twitch(
                            session, access_token, CLIENT_ID, canal_twitch
                        )
                    except Exception as e:
                        print(f"Erro verificando Twitch ({link}): {e}")
            elif "youtube.com" in link or "youtu.be" in link:
                try:
                    online = await verificar_live_youtube(session, link)
                except Exception as e:
                    print(f"Erro verificando YouTube ({link}): {e}")

            if online:
                lives_ativas.append(f"{nome}\n<:Twitch:1416469235818827876> • {link}")

    descricao = (
        "\n\n".join(lives_ativas) if lives_ativas else "Nenhuma live ativa no momento."
    )

    embed = discord.Embed(
        title="Canais ao vivo",
        description=descricao,
        color=discord.Color.green() if lives_ativas else discord.Color.dark_gray(),
    )
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?format=webp&quality=lossless&width=950&height=950"
    )

    # Edita a mensagem existente (sem notificação)
    mensagem_existente = None
    async for msg in canal.history(limit=10):
        if msg.author == bot.user and msg.embeds:
            mensagem_existente = msg
            break

    if mensagem_existente:
        await mensagem_existente.edit(embed=embed)
    else:
        await canal.send(embed=embed)


# ======= SETUP =======


async def setup(bot):
    await bot.add_cog(Lives(bot))
    atualizar_lives.bot_reference = bot
    if not atualizar_lives.is_running():
        atualizar_lives.start()
