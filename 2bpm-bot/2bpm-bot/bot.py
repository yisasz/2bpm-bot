import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime
from acoes import EscalarView, EscalarView

import random


from lives import atualizar_lives
from registro import BotaoRegistro

# ======= CONFIGURAÇÕES =======
LIMITE_USO_SEMANAL = 3  # Quantas vezes o cara pode usar antes de começar o sarcasmo

# ========= FUNÇÕES DE PERSISTÊNCIA ========= #

CAMINHO_LIVES = "lives_registradas.json"
CAMINHO_USUARIOS = "usuarios.json"
CAMINHO_ACOES = "acoes.json"
CAMINHO_ACAO = "acao_ativa.json"


def salvar_acao(texto):
    with open(CAMINHO_ACAO, "w", encoding="utf-8") as f:
        json.dump({"acao": texto}, f)


def carregar_acao():
    try:
        with open(CAMINHO_ACAO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("acao")
    except FileNotFoundError:
        return None


def salvar_em_arquivo(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def carregar_arquivo(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def carregar_acoes():
    if os.path.exists(CAMINHO_ACOES):
        with open(CAMINHO_ACOES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


# Salvar ações no arquivo
def salvar_acoes(acoes):
    with open(CAMINHO_ACOES, "w", encoding="utf-8") as f:
        json.dump(acoes, f, ensure_ascii=False, indent=4)


acoes_ativas = carregar_acoes()

contador_acoes = len(acoes_ativas) + 1


# ====== SEU ID (troque pelo seu Discord ID) ====== #
MEU_ID = 000  # Substitua aqui pelo seu ID
CANAL_ACAO_ID = 000
CANAL_ESCALACAO_ID = 000
CARGO_MENCAO_ID = 000


@tasks.loop(minutes=1)
async def reset_semanal():
    agora = datetime.now()
    if (
        agora.weekday() == 6 and agora.hour == 23 and agora.minute == 59
    ):  # Domingo 23:59
        global acoes_ativas, contador_acoes
        if acoes_ativas:
            print("[RESET SEMANAL] Zerando todas as ações da semana.")
            acoes_ativas = {}
            contador_acoes = 1
            salvar_acoes(acoes_ativas)


@reset_semanal.before_loop
async def antes_do_reset_semanal():
    await bot.wait_until_ready()


# ========= CONFIG BOT ========= #

OWNER_ID = 675907554064465930  # Ajuste seu ID aqui

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

CAMINHO_USO_COMANDOS = "uso_comandos.json"
usuarios = carregar_arquivo(CAMINHO_USUARIOS)
lives_registradas = carregar_arquivo(CAMINHO_LIVES)
uso_comandos = carregar_arquivo(CAMINHO_USO_COMANDOS)
CAMINHO_ACAO = "acao_atual.json"


def is_owner(ctx):
    return ctx.author.id == OWNER_ID


# ======= CONTAGEM DE USO COMANDOS ======= #


def incrementar_uso(user_id, comando):
    hoje = datetime.now()
    semana_atual = hoje.strftime("%Y-%W")  # ano-semana ex: 2025-24
    if user_id not in uso_comandos:
        uso_comandos[user_id] = {}
    if semana_atual not in uso_comandos[user_id]:
        uso_comandos[user_id] = {semana_atual: {"crimes": 0, "prender": 0}}
    uso_comandos[user_id][semana_atual][comando] += 1
    salvar_em_arquivo(CAMINHO_USO_COMANDOS, uso_comandos)


def verificar_sarcasmo(user_id, comando):
    hoje = datetime.now()
    semana_atual = hoje.strftime("%Y-%W")
    try:
        return uso_comandos[user_id][semana_atual][comando]
    except KeyError:
        return 0


@tasks.loop(hours=1)
async def resetar_uso_comandos():
    agora = datetime.now()
    if agora.weekday() == 0 and agora.hour == 0:  # segunda-feira 00h
        global uso_comandos
        uso_comandos = {}
        salvar_em_arquivo(CAMINHO_USO_COMANDOS, uso_comandos)
        print("🔄 Contagem de uso de comandos resetada (nova semana).")


@bot.command()
async def prender(ctx):
    user_id = str(ctx.author.id)
    uso_comandos.setdefault(user_id, {"crimes": 0, "prender": 0})

    uso_comandos[user_id]["prender"] += 1
    salvar_em_arquivo(CAMINHO_USO_COMANDOS, uso_comandos)

    if uso_comandos[user_id]["prender"] > LIMITE_USO_SEMANAL:
        frases_sarcasticas = [
            "😑 De novo perguntando o que pode prender? Vai decorar ou quer que eu desenhe?",
            "🤡 Parece que temos um amante das apreensões por aqui...",
            "😂 Mais uma vez? Vou começar a cobrar por consulta...",
            "😂 Mas tu é bisonho em...",
            "👮🏼 ah, cara... paga 10 vai!.",
        ]
        await ctx.send(random.choice(frases_sarcasticas))


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user} e comandos de barra sincronizados.")

    # Registrar views persistentes
    for acao_id in acoes_ativas.keys():
        bot.add_view(EscalarView(bot, acao_id, acoes_ativas, salvar_acoes))

    bot.add_view(BotaoRegistro(bot))  # registrar sempre

    print("✅ Views persistentes registradas.")

    if not reset_semanal.is_running():
        reset_semanal.start()

    if not resetar_uso_comandos.is_running():
        resetar_uso_comandos.start()

    # Inicia o loop de atualização das lives
    from lives import atualizar_lives

    atualizar_lives.bot_reference = bot
    if not atualizar_lives.is_running():
        atualizar_lives.start()


# ========= INICIAR BOT ========= #
from acoes import Acoes

acoes_ativas = carregar_acoes()


async def setup(bot):
    await bot.add_cog(Acoes(bot, acoes_ativas, salvar_acoes))


async def main():
    async with bot:
        await setup(bot)
        await bot.load_extension("advdiscord")
        await bot.load_extension("provas")
        await bot.load_extension("perimetro")
        await bot.load_extension("registro")
        await bot.load_extension("crimes")
        await bot.load_extension("lives")
        await bot.load_extension("programacao")
        await bot.load_extension("prenderlist")
        await bot.load_extension("promocoes")
        await bot.load_extension("comandos.unidades")
        await bot.load_extension("advertencia")
        await bot.load_extension("exoneracao")
        await bot.load_extension("curso")
        await bot.load_extension("residual")
        await bot.start("token_do_bot")  # Inicia o bot corretamente


asyncio.run(main())
