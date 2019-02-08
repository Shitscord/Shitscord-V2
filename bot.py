from discord.ext import commands
import discord, tokens, os

#Loading all cog files from /cogs
extensions=[]
for cogfile in os.listdir("cogs"):
    if str(cogfile).endswith(".py"):
        extensions.append(cogfile[:-3])


client = commands.Bot(command_prefix='!', case_insenghjgjsitive=True)

#On connection
@client.event
async def on_ready():
    print('Bot is online and connected to Discord') 

#Load and unload cog commands
@client.command()
async def load(extensions):
    try:
        client.load_extension(extension)
        print('Loaded', extension)
    except Exception as error:
        print('Cannot load:', extension, error)

@client.command()
async def unload(extensions):
    try:
        client.unload_extension(extension)
        print('Unloaded', extension)
    except Exception as error:
        print('Cannot unload:', extension, error)

#Importing/enabling cogs from extensions list
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension("cogs."+extension)
        except Exception as error:
            print('Cannot load:', extension, error)

client.run(tokens.discord)

