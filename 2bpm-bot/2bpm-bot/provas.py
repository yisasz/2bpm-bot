import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime
import json
import os
import asyncio

# IDs de configuração
USUARIO_AUTORIZADO_ID = 000  # Seu ID
CANAL_DESTINO_ID = 000  # Canal de destino
ARQUIVO_DADOS = "prova_atual.json"  # Arquivo para salvar os dados da prova


# Função auxiliar para converter string de data em datetime
def parse_data(data_str):
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None


class ProvaModal(discord.ui.Modal, title="Registro de Prova"):
    data_inicio = discord.ui.TextInput(
        label="Data de início do período",
        placeholder="Exemplo: 10/11/2025",
        style=discord.TextStyle.short,
    )
    data_termino = discord.ui.TextInput(
        label="Data de término do período",
        placeholder="Exemplo: 15/11/2025",
        style=discord.TextStyle.short,
    )
    aplicadores = discord.ui.TextInput(
        label="Nome(s) dos aplicadores",
        placeholder="Separe por vírgula se forem vários",
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        canal_destino = interaction.client.get_channel(CANAL_DESTINO_ID)

        if canal_destino is None:
            await interaction.response.send_message(
                "❌ Canal de destino não encontrado. Verifique o ID configurado.",
                ephemeral=True,
            )
            return

        data_inicio = parse_data(self.data_inicio.value)
        data_termino = parse_data(self.data_termino.value)
        hoje = datetime.now()

        # Determina status inicial
        if not data_inicio or not data_termino:
            status = "⚠️ Datas inválidas"
            cor = discord.Color.orange()
        elif hoje < data_inicio:
            status = "🟡 Aguardando início"
            cor = discord.Color.gold()
        elif data_inicio <= hoje <= data_termino:
            status = "🟢 Em andamento"
            cor = discord.Color.green()
        else:
            status = "🔴 Encerrado"
            cor = discord.Color.red()

        # Cria o embed
        embed = discord.Embed(title="📘 Período de Provas", color=cor)
        embed.add_field(
            name="📅 Período:",
            value=f"🟢 **Início:** {self.data_inicio.value}\n🔴 **Término:** {self.data_termino.value}",
            inline=False,
        )
        embed.add_field(
            name="👩‍🏫 Aplicadores:", value=self.aplicadores.value, inline=False
        )
        embed.add_field(name="📊 Status:", value=status, inline=False)

        # Envia o embed no canal
        msg = await canal_destino.send(embed=embed)

        # Salva os dados no arquivo JSON
        dados = {
            "canal_id": CANAL_DESTINO_ID,
            "mensagem_id": msg.id,
            "data_inicio": self.data_inicio.value,
            "data_termino": self.data_termino.value,
            "aplicadores": self.aplicadores.value,
        }

        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        await interaction.response.send_message(
            "✅ Período de prova registrado e monitorado automaticamente!",
            ephemeral=True,
        )


class Prova(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verificar_status_prova.start()  # Inicia a tarefa automática

    def cog_unload(self):
        self.verificar_status_prova.cancel()

    @app_commands.command(
        name="prova", description="Registrar um novo período de provas."
    )
    async def prova(self, interaction: discord.Interaction):
        if interaction.user.id != USUARIO_AUTORIZADO_ID:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        modal = ProvaModal()
        await interaction.response.send_modal(modal)

    # Tarefa automática que verifica a cada 10 minutos se o período acabou
    @tasks.loop(minutes=10)
    async def verificar_status_prova(self):
        if not os.path.exists(ARQUIVO_DADOS):
            return

        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        data_termino = parse_data(dados["data_termino"])
        data_inicio = parse_data(dados["data_inicio"])
        hoje = datetime.now()

        # Determina status atual
        if not data_inicio or not data_termino:
            return

        if hoje < data_inicio:
            status = "🟡 Aguardando início"
            cor = discord.Color.gold()
        elif data_inicio <= hoje <= data_termino:
            status = "🟢 Período em andamento"
            cor = discord.Color.green()
        else:
            status = "🔴 Período encerrado"
            cor = discord.Color.red()

        canal = self.bot.get_channel(dados["canal_id"])
        if canal is None:
            return

        try:
            msg = await canal.fetch_message(dados["mensagem_id"])
        except discord.NotFound:
            return

        # Pega o embed existente
        embed = msg.embeds[0]
        if not embed:
            return

        # Atualiza cor e status
        embed.color = cor
        for field in embed.fields:
            if field.name == "📊 Status:":
                embed.set_field_at(
                    embed.fields.index(field),
                    name="📊 Status:",
                    value=status,
                    inline=False,
                )
                break

        # Atualiza a mensagem se o status mudou
        await msg.edit(embed=embed)

    @verificar_status_prova.before_loop
    async def before_task(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Prova(bot))
