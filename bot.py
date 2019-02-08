from discord.ext import commands
import discord, tokens, constants

Client = discord.Client()
client = commands.Bot(command_prefix="")

@client.event
async def on_ready():
    print("Bot is online and connected to Discord")  # When Bot Connects

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        constants.run_coro(client.send_message(message.channel, "test"), client)


client.run(tokens.discord)

