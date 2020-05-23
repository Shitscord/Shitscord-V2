from discord.ext import commands
import discord, os

#Check if running in heroku with environment variables. If not, load variables from file
if "isHeroku" not in os.environ:
    print("Loading vars from .env")
    from dotenv import load_dotenv
    load_dotenv()

#Loading all cog files from /cogs
print("Loading Cogs")
extensions=[]
for cogfile in os.listdir("cogs"):
    if str(cogfile).endswith(".py"):
        extensions.append(cogfile[:-3])

client = commands.Bot(command_prefix='!')
testvar=1

#On connection
@client.event
async def on_ready():
    print('Bot is online and connected to Discord') 

#Importing/enabling cogs from extensions list
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension("cogs."+extension)
        except Exception as error:
            print('Cannot load:', extension, error)

discordToken = os.getenv("discordToken")
client.run(discordToken)

