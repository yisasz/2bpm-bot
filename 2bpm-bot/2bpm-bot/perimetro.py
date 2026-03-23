import discord
from discord.ext import commands
from discord import app_commands

opcoes = {
    "1": {
        "label": "Açougue",
        "titulo": "Perímetro do Açougue",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** 7\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 10\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1384152636441235591/1385462536052412457/image.png",
    },
    "2": {
        "label": "Joalheria",
        "titulo": "Perímetro da Joalheria",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 | Máx 11 \n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Fuzil",
        "imagem": "https://media.discordapp.net/attachments/1384152636441235591/1385450065329651842/image.png",
    },
    "3": {
        "label": "Madeireira",
        "titulo": "Perímetro da Madeireira",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs:** 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 10\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1384152636441235591/1385489397646098482/image.png",
    },
    "4": {
        "label": "Galinheiro",
        "titulo": "Perímetro do Galinheiro",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs:** 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 10\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ:** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1384152636441235591/1385496379194867764/image.png",
    },
    "5": {
        "label": "Banco Central",
        "titulo": "Perímetro do Banco Central.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs:** Min 10 | Máx 14\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 16 | Máx 19\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ:** Fuzil",
        "imagem": "https://cdn.discordapp.com/attachments/1012421448352153678/1385492764279574658/image.png?ex=68924070&is=6890eef0&hm=cde00232af7d298da354f8810946396f892ec002ef6c731dcece127786925d97&",
    },
    "6": {
        "label": "Fleeca (Praia)",
        "titulo": "Perímetro do Fleeca (Praia)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs:** Min 6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 | Máx 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Fuzil",
        "imagem": "https://media.discordapp.net/attachments/1384152636441235591/1385491051095134248/image.png",
    },
    "7": {
        "label": "Fleeca (Paleto)",
        "titulo": "Perímetro do Fleeca (Paleto)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: **Min  6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 | Máx 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Fuzil",
        "imagem": "https://media.discordapp.net/attachments/1384152636441235591/1385456705789362176/image.png",
    },
    "8": {
        "label": "Fleeca (Chaves)",
        "titulo": "Perímetro do Fleeca (Chaves)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 Máx 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Fuzil",
        "imagem": "https://cdn.discordapp.com/attachments/1382462214799229008/1385688918963519498/image.png?ex=687e87df&is=687d365f&hm=97acd161aaf954d7e01030febbc599096f954e600379f6cf4e09d45e5b6aa29d&",
    },
    "9": {
        "label": "Fleeca (Rota 68)",
        "titulo": "Perímetro do Fleeca (Rota 68)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 6 Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 | Máx 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Fuzil",
        "imagem": "https://media.discordapp.net/attachments/1382462214799229008/1385689044997902446/image.png?ex=687e87fd&is=687d367d&hm=456e511412fe7c93b283865f6744c867fb3bab2d33f5e6b445dd2a40b64f3094&",
    },
    "10": {
        "label": "Fleeca (Shopping)",
        "titulo": "Perímetro do Fleeca (Shopping)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 | Máx 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ:** Fuzil",
        "imagem": "https://cdn.discordapp.com/attachments/1382462214799229008/1385688594860998666/image.png?ex=687e8791&is=687d3611&hm=9c0e0df3f36414666b4e5aaeec9de3dea43dcec2bc2f1e7b39ee0e317efe39c3&",
    },
    "11": {
        "label": "Ferro Velho (Sul)",
        "titulo": "Perímetro do Ferro-Velho (Sul)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** 5\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 7\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas e SMG",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401655191106748498/image.png?ex=6892621f&is=6891109f&hm=dfa8174a3b0548bf9b0a00ca96ee4e7f6bffb1d005c7d8c2a98abb6a41d0b053&",
    },
    "12": {
        "label": "Ferro Velho (Norte)",
        "titulo": "Perímetro do Ferro-Velho (Norte)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** 5\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 7\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas e SMG",
        "imagem": "https://cdn.discordapp.com/attachments/1384152636441235591/1385499821921534063/image.png?ex=687e8082&is=687d2f02&hm=a552e89038e80a1c1442f0fea6510fe9770164933c797f9cd3fc5893beab7b19&",
    },
    "13": {
        "label": "Aeroporto do Norte",
        "titulo": "Perímetro do Aeroporto do Norte",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 10\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas e Tec-nine",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1395851969100513290/image.png?ex=687e96f3&is=687d4573&hm=8bed331636e78a4c1cef023331bc8073151605241a10da4425b0a5fca7267d18&format=webp&quality=lossless&",
    },
    "14": {
        "label": "Fleeca (Campo de Golfe)",
        "titulo": "Perímetro do Fleeca (Campo de Golfe)",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 6 | Máx 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 9 Máx | 11\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas e Tec-nine",
        "imagem": "https://cdn.discordapp.com/attachments/1382462214799229008/1385688177460908163/image.png?ex=687e872e&is=687d35ae&hm=b656bc0f063692b58695c5af1009ef3017b5b235480e25bcbe0ca9917074d46c&",
    },
    "15": {
        "label": "Roubo ao Zancudo",
        "titulo": "Assalto ao Zancudo",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** 8\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** 10\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Tec-nine",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1394820651319169094/image.png",
    },
    "16": {
        "label": "Lojinha do Vanilla",
        "titulo": "Perímetro Lojinha do Vanilla.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401630527022436384/image.png?ex=6890f9a6&is=688fa826&hm=737255943c3fcd6528bae1763709f951ef4bba039b73431345cf0454822fc26b&=&format=webp&quality=lossless",
    },
    "17": {
        "label": "Lojinha Rodovia Arcanjos",
        "titulo": "Perímetro Lojinha Rodovia Arcanjos.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401631484112146514/image.png?ex=68924c0a&is=6890fa8a&hm=1e4dea867c1a332e6197a1ebb48a2907316da9987eef0134bf3a1985565da47a&=&format=webp&quality=lossless",
    },
    "18": {
        "label": "Lojinha de Mirror Park",
        "titulo": "Perímetro Lojinha de Mirror Park.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401632399477182514/image.png?ex=68924ce5&is=6890fb65&hm=ed681575342e4ea65815bbe91aff772b1ca0d98ef189fae17000d89d38414c5d&=&format=webp&quality=lossless",
    },
    "19": {
        "label": "Lojinha do China",
        "titulo": "Perímetro Lojinha do China.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401632773994713249/image.png?ex=68924d3e&is=6890fbbe&hm=534d3a39863943e0f31eba5aa23c15761156bd165300f5bd9479000746bd644b&=&format=webp&quality=lossless",
    },
    "20": {
        "label": "Lojinha dos Ballas",
        "titulo": "Perímetro Lojinha dos Ballas.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401634763877384262/image.png?ex=68924f18&is=6890fd98&hm=c89e46201af31fd01b3d70fe27f6937e835ec51438c65cf425965fbd12ed3509&=&format=webp&quality=lossless",
    },
    "21": {
        "label": "Lojinha do Central",
        "titulo": "Perímetro Lojinha do Central.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401636451200012318/image.png?ex=689250ab&is=6890ff2b&hm=94f18c722c35bbe2ef117c1b6ca7b68f33b32d16be046c0fb54a6974251dd25a&=&format=webp&quality=lossless",
    },
    "22": {
        "label": "Lojinha da Praia",
        "titulo": "Perímetro Lojinha da Praia.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401636964431822918/image.png?ex=68925125&is=6890ffa5&hm=3d7cf2a04b3d9032ed5d9e0cdc0135c02294a02e05218e2bde35156ec15c12e1&=&format=webp&quality=lossless",
    },
    "23": {
        "label": "Lojinha do Pops",
        "titulo": "Perímetro Lojinha do Pops.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401637304082104515/image.png?ex=68925176&is=6890fff6&hm=c9143ec0bfdd8607fab4efe8a98fe4a7d032c6a188a9907d281c5cf9ded4fd12&",
    },
    "24": {
        "label": "Lojinha do Ark",
        "titulo": "Perímetro Lojinha do Ark.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401637602754560061/image.png?ex=689251bd&is=6891003d&hm=87521aed468bd7acfee83366e84874760ef0ca17725b91155360764c491c4260&",
    },
    "25": {
        "label": "Lojinha de Sandy",
        "titulo": "Perímetro Lojinha de Sandy.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401638667943940208/image.png?ex=689252bb&is=6891013b&hm=29c2b84b80573368e552cb4b6d3e4773f1e0b3fdfeba1efc4033d2989902f406&",
    },
    "26": {
        "label": "Lojinha do Yellowjack",
        "titulo": "Perímetro Lojinha do Yellowjack.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401639025520935002/image.png?ex=68925310&is=68910190&hm=804a23728d8bbdb608adfd2e30fbeebaec34ddde7301ebba1ea97f98697a0059&=&format=webp&quality=lossless",
    },
    "27": {
        "label": "Lojinha de Grape",
        "titulo": "Perímetro Lojinha de Grape.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://media.discordapp.net/attachments/1392602446747930664/1401639339691212940/image.png?ex=6892535b&is=689101db&hm=ce6adc9e79531b509a0e9b362ac1ca251ec9c3fb0133f16a4983facf8d94e11e&=&format=webp&quality=lossless",
    },
    "28": {
        "label": "Lojinha da Universidade",
        "titulo": "Perímetro Lojinha da Universidade.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401639617563852840/image.png?ex=6892539e&is=6891021e&hm=165dbf2411fbd42acafdc6fa8b88c08e8c771a895b37f09090082017cfd5d932&",
    },
    "29": {
        "label": "Lojinha do Naturali",
        "titulo": "Perímetro Lojinha do Naturali.",
        "descricao": "**:man_detective: ʙᴀɴᴅɪᴅᴏs: ** Min 3 | Máx 4\n**:police_car: ᴘᴏʟɪᴄɪᴀɪs: ** Min 4 Máx | 5\n**<:gun:1396168984117903520> ᴀʀᴍᴀᴍᴇɴᴛᴏ: ** Pistolas",
        "imagem": "https://cdn.discordapp.com/attachments/1392602446747930664/1401641121939066930/image.png?ex=68925504&is=68910384&hm=04ef8db21243a82114f6dacdad4ea7ca0c5b030b4e09bd2a645c346140297ef9&",
    },
}


class Perimetro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class PerimetroSelect(discord.ui.Select):
        def __init__(self, options, opcoes, nome_categoria):
            super().__init__(
                placeholder=f"📁 {nome_categoria}...",
                min_values=1,
                max_values=1,
                options=options,
            )
            self.opcoes = opcoes

        async def callback(self, interaction: discord.Interaction):
            escolha = self.values[0]
            dados = self.opcoes[escolha]

            embed = discord.Embed(
                title=dados["titulo"],
                description=dados["descricao"],
                color=discord.Color.from_rgb(153, 0, 0),
            )
            embed.set_author(
                name="Consulta de Perímetro.",
                icon_url="https://cdn-icons-png.flaticon.com/512/684/684908.png",
            )
            embed.set_image(url=dados["imagem"])
            embed.set_footer(
                text=f"Solicitado por {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url,
            )

            await interaction.response.send_message(embed=embed)

    class PerimetroDropdown(discord.ui.View):
        def __init__(self, opcoes):
            super().__init__(timeout=60)

            categorias = {
                "Assaltos médios/grandes": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                ],
                "Lojas de Departamento": [
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                ],
            }

            for nome_categoria, chaves in categorias.items():
                options = [
                    discord.SelectOption(label=opcoes[chave]["label"], value=chave)
                    for chave in chaves
                    if chave in opcoes
                ]

                if options:
                    select = Perimetro.PerimetroSelect(options, opcoes, nome_categoria)
                    self.add_item(select)

    @app_commands.command(name="perimetro", description="Consultar perímetros de ações")
    async def perimetro(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=self.embed_opcoes(),
            view=Perimetro.PerimetroDropdown(opcoes),
        )

    def embed_opcoes(self):
        return discord.Embed(
            title="📋 Selecione o Perímetro",
            description="Escolha uma categoria no menu abaixo para consultar os perímetros disponíveis.",
            color=discord.Color.blurple(),
        )


async def setup(bot):
    await bot.add_cog(Perimetro(bot))
