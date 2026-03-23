# arquivo: curso.py
import discord
from discord import app_commands
from discord.ext import commands


class Curso(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # IDs permitidos para usar o comando
        self.allowed_users = [
            000,  # ID do cargo permitido (pode adicionar mais IDs de cargos aqui)
            000,
        ]
        # IDs de cargos que podem ser atribuídos
        self.allowed_roles = [
            000,  # ID do cargo permitido (pode adicionar mais IDs de cargos aqui)
            000,
        ]
        # Canal para logs
        self.log_channel_id = 1401348355044540456  # Coloque aqui o ID do canal de logs

    async def role_autocomplete(self, interaction: discord.Interaction, current: str):
        roles = [
            role
            for role in interaction.guild.roles
            if role.id in self.allowed_roles and current.lower() in role.name.lower()
        ]
        return [
            app_commands.Choice(name=role.name, value=str(role.id))
            for role in roles[:25]
        ]

    async def member_autocomplete(self, interaction: discord.Interaction, current: str):
        members = [
            member
            for member in interaction.guild.members
            if current.lower() in member.display_name.lower()
            or current.lower() in member.name.lower()
        ]
        return [
            app_commands.Choice(name=member.display_name, value=str(member.id))
            for member in members[:25]
        ]

    @app_commands.command(
        name="curso", description="Atribui um cargo para até 10 usuários."
    )
    @app_commands.describe(
        cargo="Selecione o cargo",
        usuario1="Usuário 1",
        usuario2="Usuário 2",
        usuario3="Usuário 3",
        usuario4="Usuário 4",
        usuario5="Usuário 5",
        usuario6="Usuário 6",
        usuario7="Usuário 7",
        usuario8="Usuário 8",
        usuario9="Usuário 9",
        usuario10="Usuário 10",
    )
    @app_commands.autocomplete(
        cargo=role_autocomplete,
        usuario1=member_autocomplete,
        usuario2=member_autocomplete,
        usuario3=member_autocomplete,
        usuario4=member_autocomplete,
        usuario5=member_autocomplete,
        usuario6=member_autocomplete,
        usuario7=member_autocomplete,
        usuario8=member_autocomplete,
        usuario9=member_autocomplete,
        usuario10=member_autocomplete,
    )
    async def curso(
        self,
        interaction: discord.Interaction,
        cargo: str,
        usuario1: str = None,
        usuario2: str = None,
        usuario3: str = None,
        usuario4: str = None,
        usuario5: str = None,
        usuario6: str = None,
        usuario7: str = None,
        usuario8: str = None,
        usuario9: str = None,
        usuario10: str = None,
    ):

        if interaction.user.id not in self.allowed_users:
            return await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.", ephemeral=True
            )

        role = interaction.guild.get_role(int(cargo))
        if not role:
            return await interaction.response.send_message(
                "❌ Cargo inválido.", ephemeral=True
            )

        user_ids = [
            usuario1,
            usuario2,
            usuario3,
            usuario4,
            usuario5,
            usuario6,
            usuario7,
            usuario8,
            usuario9,
            usuario10,
        ]
        user_ids = [uid for uid in user_ids if uid is not None]

        if not user_ids:
            return await interaction.response.send_message(
                "❌ Nenhum usuário selecionado.", ephemeral=True
            )

        falhas = []
        sucesso = []

        for uid in user_ids:
            member = interaction.guild.get_member(int(uid))
            if member:
                try:
                    await member.add_roles(role)
                    sucesso.append(member.display_name)
                except Exception as e:
                    falhas.append(member.display_name)
            else:
                falhas.append(f"ID {uid}")

        # Envia feedback
        feedback = (
            f"✅ Cargo **{role.name}** atribuído com sucesso para: {', '.join(sucesso)}\n"
            if sucesso
            else ""
        )
        if falhas:
            feedback += f"⚠ Falha ao atribuir para: {', '.join(falhas)}"

        await interaction.response.send_message(feedback, ephemeral=True)

        # Log
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            embed = discord.Embed(title="📋 Log de /curso", color=discord.Color.blue())
            embed.add_field(
                name="Executor", value=interaction.user.mention, inline=False
            )
            embed.add_field(name="Cargo", value=role.name, inline=False)
            if sucesso:
                embed.add_field(name="Sucesso", value=", ".join(sucesso), inline=False)
            if falhas:
                embed.add_field(name="Falhas", value=", ".join(falhas), inline=False)
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Curso(bot))
