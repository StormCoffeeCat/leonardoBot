# imports
import os
import openai
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# openai setup
openai.organization = 'org-y8b1gmfkEMElgOyjjRG1s5PX'
openai.api_key = os.getenv('KEY')

# discord setup
bot = commands.Bot(command_prefix='./', intents=discord.Intents.all(), help_command=None)

# remove the existing command tree from the bot instance
bot.command_tree = None

# create the CommandTree object for the bot
tree = app_commands.CommandTree(bot)

# define your commands using the @tree.command decorator
@tree.command(name='ping', description='Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@bot.event
async def on_ready():
  await tree.sync()
  print('Bot is ready')

# bot checks for message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('./'):
        return
    prompt = message.content

    # prompts the ai to generate a response
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.8)

    # sends the response to the channel
    await message.channel.send(completion.choices[0].text)

# run bot
bot.run(os.getenv('TOKEN'))
