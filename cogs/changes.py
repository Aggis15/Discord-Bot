import discord
from discord.ext import commands


class changes(commands.Cog):
    def __init__(self, Client):
        self.Client = Client


    @commands.command()
    @commands.is_owner()
    async def changes(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = "New changes!",
            description = "∙ Added ``!guildinfo`` command to show Guild (server) Info. \n ∙ Added ``!memberinfo`` command to show specified member information. NOTE: You must ping someone (even yourself) or else the command will throw an error. \n ∙ Changed the way someone can verify they have read the rules.",
            color = discord.Color.blurple()
        )
        embed.set_author(name = "Workout Workplace", icon_url = "https://cdn.discordapp.com/attachments/734879286023946240/737404555058348112/workout_workplace.jpg")
        embed.set_footer(text = "Date changes were applied: 5/10/2020" )

        await ctx.send(embed=embed)


def setup(Client):
    Client.add_cog(changes(Client))