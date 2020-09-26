import discord
from discord.ext import commands
from discord.utils import get
import logging
import time
from datetime import date
from dotenv import load_dotenv
import os
import asyncio
import keep_alive
load_dotenv()


activity = discord.Activity(type=discord.ActivityType.watching, name="you work out!")
status = discord.Status.online
Client = commands.Bot(command_prefix="!")
t = time.localtime()
clock = time.strftime("%H:%M:%S", t)
today = date.today()
date = today.strftime("%m-%d-%Y")
token = os.getenv("Token")

# Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# When bot is ready event
@Client.event
async def on_ready():
	print(f' {Client.user} has successfully connected to Discord! Current time: ' + clock + " UTC")
	await Client.change_presence(status=status, activity=activity)
	print(f"Status has been changed to \"{status}\" and activity to \"{activity}\"")

# When someone joins the server, it gets printed in the join channel and in the console
@Client.event
async def on_member_join(member):
	# Channel ID's
	joinchannel = Client.get_channel(735063988861272185)
	dmchannel = await member.create_dm()
	staffchannel = Client.get_channel(735064782377451533)
	# Log Embed
	logembed = discord.Embed (
		title = "Member joined",
		description = f"{member} has joined the server. \n Account created at: {member.created_at}",
		color = discord.Colour.blue()
	)
	logembed.set_footer(text = f"ID: {member.id} • " + date + " M-D-Y")
	# DM embed
	dmembed = discord.Embed (
		title = "Workout Workplace",
		description = "Please react with the :muscle: emoji (muscle) in order to get access to the server. By reacting, you agree that you have read and agree to the rules!",
		colour = discord.Colour.blue()
	)
	# Gets the role name 
	role = get(member.guild.roles, name="Athletes")
	# Welcome channel message
	await joinchannel.send(f"Welcome to the **Workout Workplace** {member.mention}! Please go over #rules and check your Direct Messages for further instructions! Looking forward to seeing you around!"),
	# Logs it in the console
	print(f"{member} has joined the server!")
	# Staff channel embed 
	await staffchannel.send(embed=logembed)
	# Sends a DM to the user that joined
	await dmchannel.send(embed=dmembed)
	# Wait for a reaction and add role
	await Client.wait_for("reaction_add")
	await member.add_roles(role)
	print(f"{member} has reacted to the DM message and has been given access to the server!")
	

# When someone leaves the server, it gets printed in the staff channel and in the console
@Client.event 
async def on_member_remove(member):
	# Gets channel ID
	leavechannel = Client.get_channel(735064782377451533)
	# Embed Format
	embed = discord.Embed(
		title = "Member left",
		description = f"{member} has left the server! \n Joined at: {member.joined_at}",
		colour = discord.Colour.blue()
	)
	embed.set_footer(text = f"ID: {member.id} • " + date + " M-D-Y")
	# Sends the message 
	await leavechannel.send(embed=embed)
	# Logs it in the console
	print(f"{member} has left the server!")


# Shows ping between Discord and bot
@Client.command()
async def ping(ctx):
	message = await ctx.send("Pong!")
	await asyncio.sleep(0.4)
	await message.edit(content=f"Pong! Bot ping is ``{round(Client.latency * 1000)}ms``")
	print(f"Ping command was used by \"{ctx.author.name}\".")
	if Client.latency <= 200:
		await message.edit(content=f"Pong! Bot ping is ``{round(Client.latency * 1000)}ms``. That's great!")
	elif Client.latency >= 500:
		await ctx.send(content=f"Pong! Bot ping is ``{round(Client.latency * 1000)}ms``. That's not too great. :(")



# Repeats all arguments after the command
@Client.command()
@commands.has_role("Moderators")
async def echo(ctx, *, arg):
	message = ctx.message
	await ctx.send(arg)
	await message.delete()
	print(f"Echo command was used by \"{ctx.author.name}\" and said \"{arg}\"!")

# The rules embed and reactions 
@Client.command()
@commands.has_role("Moderators")
async def Rules(ctx):
	embed=discord.Embed(
		title = "Server rules",
		description = """1. No harassment, homophobia, transphobia or racism whatsoever. Heavy slurs are also counted towards harrasement. That also goes if you say negative stuff about someone else's success. We all started from somewhere. If you are unsure if you should say something, don't.
2. No spam. That means no hundreds of messages for one sentence, no excessive caps etc.
3. No NSFW in ANY of the channels. This will result in an instant warning and mute.
4. Be mindful of all channels and their uses.
5. No drama in ANY of the channels. If there is drama, take it to DM's. Also ping an online moderator.
6. If a staff member tells you to stop doing something, you should do it, no questions asked.
7. No backseat modding. If there is something going on that needs the attention of a moderator, ping an online moderator. Don't take the situation in your own hands. Doing that will result in an instant warning and mute.
8. Do not type in any other language other than English. Typing in any other language will result in an instant warning or mute.
9. All nicknames should be mentionable.
10. No advertisement without given permission. That includes DM's as well..

After 3 official warnings, you will be temporarily banned for 7 days. After you return, your first offence will result in a permanent ban.

Depending on the severity of the offence, you might be soft warned (verbal warning) or immediately temporarily banned for 4 days.""",
		colour = discord.Colour.blue()
	)

	embed.set_footer(text="We hope you enjoy your stay!")
	embed.set_author(name="Workout Workplace", icon_url="https://cdn.discordapp.com/attachments/734879286023946240/737404555058348112/workout_workplace.jpg")
	
	await ctx.send(embed=embed)


# Opens the cogs file and registers the cogs
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		Client.load_extension(f"cogs.{filename[:-3]}")

# Starts the server
keep_alive.keep_alive()


# Starts the bot
Client.run (token)
