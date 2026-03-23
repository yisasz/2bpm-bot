import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands

from utils import salvar_em_arquivo, CAMINHO_USO_COMANDOS, uso_comandos

LIMITE_USO_SEMANAL = 3


class Crimes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="crimes", description="Consultar penalidades de crimes na cidade."
    )
    async def crimes(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        uso_comandos.setdefault(user_id, {"crimes": 0, "prender": 0})
        uso_comandos[user_id]["crimes"] += 1
        salvar_em_arquivo(CAMINHO_USO_COMANDOS, uso_comandos)

        frases_sarcasticas = [
            "🤨 De novo esse comando? Já decorou os crimes ou quer um diploma?",
            "😒 Acho que você já sabe isso de cor... mas tudo bem né...",
            "🙄 Tá querendo montar um currículo criminal ou o que?",
            "😂 Mas tu é bisonho em...",
            "👮🏼 ah, cara... paga 10 vai!.",
        ]

        # Respostas para os crimes
        respostas = {
            "atm": discord.Embed(
                title="🔎 Detalhes da Infração - ATM",
                color=0xB00020,  # Vermelho escuro (alerta)
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )  # Ícone de alerta, opcional
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Roubo de caixa eletrônico (ATM)\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de Fuga\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```10```", inline=True)
            .add_field(name="💰 Multa", value="```R$2.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```R$10.000```", inline=True),
            "nióbio": discord.Embed(
                title="🔎 Detalhes da Infração - Nióbio", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto qualificado.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Sequestro\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```50```", inline=True)
            .add_field(name="💰 Multa", value="```R$39.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "fleeca": discord.Embed(
                title="🔎 Detalhes da Infração - Fleeca", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto qualificado.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Sequestro\n- Tentativa de fuga\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```50```", inline=True)
            .add_field(name="💰 Multa", value="```R$39.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True)
            .set_footer(text="Sistema de Penalidades | Cidade dos Anjos"),
            "açougue": discord.Embed(
                title="🔎 Detalhes da Infração - Açougue", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Sequestro\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```yaml\n40\n```", inline=True)
            .add_field(name="💰 Multa", value="```yaml\nR$26.000\n```", inline=True)
            .add_field(name="⚖️ Fiança", value="```yaml\n-\n```", inline=True)
            .set_footer(text="Sistema de Penalidades | Cidade dos Anjos"),
            "lavagem": discord.Embed(
                title="🔎 Detalhes da Infração - Lavagem", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Lavagem de dinheiro.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de fuga\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```10```", inline=True)
            .add_field(name="💰 Multa", value="```R$6.500```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "barbearia": discord.Embed(
                title="🔎 Detalhes da Infração - Barbearia", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto a Barbearia.\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```10```", inline=True)
            .add_field(name="💰 Multa", value="```R$2.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```R$10.000```", inline=True),
            "desmanche": discord.Embed(
                title="🔎 Detalhes da Infração - Desmanche", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Roubo\n- Desmanche de carros.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de fuga\n- Equipamento Ilegal\n- Porte de arma de fogo\n- Associação criminosa```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```19```", inline=True)
            .add_field(name="💰 Multa", value="```R$8.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```27.000```", inline=True),
            "galinheiro": discord.Embed(
                title="🔎 Detalhes da Infração - Galinheiro", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio.\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```40```", inline=True)
            .add_field(name="💰 Multa", value="```R$26.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "madeireira": discord.Embed(
                title="🔎 Detalhes da Infração - Madeireira", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio.\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```40```", inline=True)
            .add_field(name="💰 Multa", value="```R$26.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "joalheria": discord.Embed(
                title="🔎 Detalhes da Infração - Joalheria", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto qualificado.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Sequestro\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```50```", inline=True)
            .add_field(name="💰 Multa", value="```R$39.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "ferro-velho": discord.Embed(
                title="🔎 Detalhes da Infração - Ferro-Velho", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio.\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```40```", inline=True)
            .add_field(name="💰 Multa", value="```R$26.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "registradora": discord.Embed(
                title="🔎 Detalhes da Infração - Registradora", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Furto.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de fuga\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```8```", inline=True)
            .add_field(name="💰 Multa", value="```R2.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```8.000```", inline=True),
            "banco central": discord.Embed(
                title="🔎 Detalhes da Infração - Banco Central", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto qualificado.\n```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de fuga\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="```50```", inline=True)
            .add_field(name="💰 Multa", value="```R$39.000```", inline=True)
            .add_field(name="⚖️ Fiança", value="```-```", inline=True),
            "loja de armas": discord.Embed(
                title="🔎 Detalhes da Infração - Loja de Armas", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto (lojas/ammu)\n- Porte de arma de fogo\n- Tentativa de homicídio contra servidor público```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Equipamento Ilegal```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```45```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$21.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```-```**", inline=True),
            "porte de arma": discord.Embed(
                title="🔎 Detalhes da Infração - Porte de Arma", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Porte de arma de fogo\n(apenas pistola)```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```10```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$13.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```R$23.000```**", inline=True),
            "loja de roupas": discord.Embed(
                title="🔎 Detalhes da Infração - Loja de Roupas/Tatuador",
                color=0xB00020,
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto (lojas/ammu)\n- Porte de arma de fogo\n- Tentativa de homicídio contra servidor público```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```45```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$21.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```-```**", inline=True),
            "corrida ilegal": discord.Embed(
                title="🔎 Detalhes da Infração - Corrida Ilegal", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Corrida ilegal```",
                inline=False,
            )
            .add_field(
                name="> Adicionais Possíveis:",
                value="```yaml\n- Tentativa de fuga\n- Equipamento Ilegal\n```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```3```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$4.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```R$7.000```**", inline=True),
            "aeroporto do norte": discord.Embed(
                title="🔎 Detalhes da Infração - Aeroporto do Norte", color=0xB00020
            )
            .set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=6882b65b&is=688164db&hm=ff567ee7399de7d16659d1962f2915b1a1e5076e97f3779f633fa76c63d655b2&"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio.```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```40```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$26.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```-```**", inline=True),
            "loja de departamento": discord.Embed(
                title="🔎 Detalhes da Infração - Loja de Departamento", color=0xB00020
            )
            .set_thumbnail(
                url="https://media.discordapp.net/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=68cbe19b&is=68ca901b&hm=78e0101b785e6c1dfbd1b7620c8648e4239ff0455a36c8ced53c9437881ee3e1&=&format=webp&quality=lossless&width=950&height=950"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto (lojas/ammu)\n- Associação criminosa\n- Porte de arma de fogo\n- Tentativa de homicídio contra servidor público```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```50```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$23.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```-```**", inline=True),
            ###########################################################################################
            "plataforma de petróleo": discord.Embed(
                title="🔎 Detalhes da Infração - Plataforma de Petróleo", color=0xB00020
            )
            .set_thumbnail(
                url="https://media.discordapp.net/attachments/1383190645035765841/1397709978298486804/CDA_-_LOGO_2BPM_Dos_Anjos-1.png?ex=68cbe19b&is=68ca901b&hm=78e0101b785e6c1dfbd1b7620c8648e4239ff0455a36c8ced53c9437881ee3e1&=&format=webp&quality=lossless&width=950&height=950"
            )
            .add_field(
                name="> Infrações Cometidas:",
                value="```yaml\n- Assalto médio```",
                inline=False,
            )
            .add_field(name="🛠️ Serviços", value="**```40```**", inline=True)
            .add_field(name="💰 Multa", value="**```R$26.000```**", inline=True)
            .add_field(name="⚖️ Fiança", value="**```-```**", inline=True),
        }

        # Menu de seleção
        options = [
            discord.SelectOption(label=nome.title(), value=key)
            for key, nome in zip(respostas.keys(), respostas.keys())
        ]

        class CrimesSelect(discord.ui.View):
            @discord.ui.select(
                placeholder="Escolha um crime",
                min_values=1,
                max_values=1,
                options=options,
            )
            async def select_callback(
                self, interaction_select: discord.Interaction, select: discord.ui.Select
            ):
                chave = select.values[0]
                resultado = respostas[chave]

                if isinstance(resultado, discord.Embed):
                    await interaction_select.response.send_message(embed=resultado)
                else:
                    embed = discord.Embed(
                        title=f"📌 {chave.title()}",
                        description=resultado,
                        color=0x00A8FF,
                    )
                    await interaction_select.response.send_message(embed=embed)
                self.stop()

        embed_lista = discord.Embed(
            title="> 🕵️ Consulta de Crimes",
            description="Selecione uma infração no menu abaixo para consultar detalhes como serviços, multa e fiança.",
            color=discord.Color.from_rgb(0, 92, 207),
        )
        embed_lista.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/954/954591.png"
        )
        embed_lista.set_footer(
            text="Sistema de Penalidades",
            icon_url="https://cdn-icons-png.flaticon.com/512/565/565547.png",
        )

        if uso_comandos[user_id]["crimes"] > LIMITE_USO_SEMANAL:
            frase = random.choice(frases_sarcasticas)
            await interaction.response.send_message(
                content=frase, embed=embed_lista, view=CrimesSelect()
            )
        else:
            await interaction.response.send_message(
                embed=embed_lista, view=CrimesSelect()
            )


async def setup(bot):
    await bot.add_cog(Crimes(bot))
