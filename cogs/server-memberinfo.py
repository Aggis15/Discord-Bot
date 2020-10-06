import discord
from discord.ext import commands


class memberinfo(commands.Cog):
    def __init__(self, Client):
        self.Client = Client

    @commands.command()
    async def memberinfo(self, ctx, member: discord.Member):
        boosting = False
        if member.premium_since == None:
            boosting = False
        else:
            boosting = True
        roles = [role for role in member.roles]    
        embed = discord.Embed(
                title = f"Information about {member.display_name}",
                colour = discord.Color.blurple()
            )
        embed.set_footer(text = f"User ID: {member.id}")
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_author(name = "Workout Bot",
        icon_url = "https://cdn.discordapp.com/avatars/741343821820067953/06bf4f7c19684d17e09005cea5416f12.png?size=1024")
        embed.add_field(name = "Account created at:",
        value = str(member.created_at.replace(microsecond=0)) + " UTC",
        inline = True)
        embed.add_field(name = "Joined the server at:",
        value = str(member.joined_at.replace(microsecond=0)) + " UTC",
        inline = True)
        embed.add_field(name = "Boosting",
        value = boosting,
        inline = True)
        embed.add_field(name = f"Roles {member.display_name} has:",
        value =  " ".join([role.mention for role in roles]),
        inline = True)
        await ctx.send(embed=embed)
        print (f"{ctx.author.name} checked for someone's info")


    @memberinfo.error
    async def memberinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a user in order to see information about them!")
            print ("Member Not Found Error caught at memberinfo")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send ("You need to mention a user in order to see information about them!")
            print ("Missing argument error caught at memberinfo")

    @commands.command()
    async def guildinfo (self, ctx):
        guild = ctx.message.guild
        embed = discord.Embed(
            title = f"Server information",
            description = f"Owner: {guild.owner.mention} | Region: {guild.region}",
            colour = discord.Colour.blurple()
        )
        embed.set_footer (text = f"Server ID: {guild.id} | Created at: {guild.created_at.replace(microsecond=0)}")
        embed.set_thumbnail(url = guild.icon_url)
        embed.set_author(name = guild.name,
        icon_url = guild.icon_url)
        embed.add_field(name = "Current members",
        value = len(guild.members),
        inline = True)
        embed.add_field(name = "Boosts",
        value = guild.premium_subscription_count,
        inline = True)
        embed.add_field(name = "Server level",
        value = guild.premium_tier,
        inline = True)
        embed.add_field(name = "Channels",
        value = f"Text channels: {len(guild.text_channels)} \n Voice channels: {len(guild.voice_channels)}",
        inline = True)
        embed.add_field(name = "Roles",
        value = len(guild.roles),
        inline = True)
        embed.add_field(name = "Emojis",
        value = len(guild.emojis),
        inline = True)
        print (f"{ctx.author} checked guild info")

        await ctx.send(embed=embed)
        


def setup(Client):
    Client.add_cog(memberinfo(Client))