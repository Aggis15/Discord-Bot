import discord
from discord.ext import commands
from datetime import datetime
from time import strftime

date = datetime.today().strftime("%m-%d-%Y")

class Administrative_Commands(commands.Cog):
    def __init__(self, Client):
        self.Client = Client

# Kicks pinged user and logs it in the staff chat
    @commands.command()
    @commands.has_role("Moderators")
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        log = self.Client.get_channel(735064782377451533)
        embed = discord.Embed(
            title = "Member kicked",
            description = f"{member} was kicked from the server. \n Responsible moderator: {ctx.author} \n Reason: {reason}",
            colour = discord.Color.dark_blue()
        )
        embed.set_footer(text = f"ID: {member.id} • " + date + "M-D-Y")
        embed.set_author (name = f"{member}", icon_url = f"{member.avatar_url}")


        await member.kick(reason=reason)
        await log.send(embed=embed)
        print(f"{member} was kicked from the server!")



# Bans pinged user and logs it in the staff chat
    @commands.command()
    @commands.has_role("Moderators")
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        log = self.Client.get_channel(735064782377451533)
        embed = discord.Embed(
            title = "Member banned",
            description = f"{member} was banned from the server. \n Responsible moderator: {ctx.author} \n Reason: {reason}",
            colour = discord.Color.dark_blue()
        )
        embed.set_footer(text = f"ID: {member.id} • " + date + " M-D-Y")
        embed.set_author (name = f"{member}", icon_url = f"{member.avatar_url}")
        await member.ban(reason=reason)
        await log.send(embed=embed)
        print (f"{member} has been banned from the server!")
    



    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log = self.Client.get_channel(735064782377451533)
        embed = discord.Embed(
            title = "Member Unbanned",
            description = f"{user} was unbanned from **{guild}**!",
            colour = discord.Color.dark_blue()
        )
        embed.set_footer(text = f"ID: {user.id} • " + date + " M-D-Y")
        embed.set_author (name = f"{user}", icon_url = f"{user.avatar_url}")
        await log.send(embed=embed)
        print(f"{user} was unbanned from {guild}!")


    

def setup(Client):
    Client.add_cog(Administrative_Commands(Client))