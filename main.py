# imports
import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands
import sqlite3

# load environment variables from .env file
load_dotenv()

# set OpenAI organization and API key from environment variables
openai.organization = os.getenv('ORG')
openai.api_key = os.getenv('KEY')

# initialize Discord bot with command prefix, intents, and help command
bot = commands.Bot(command_prefix='./', intents=discord.Intents.all(), help_command=None)

# event handler for when the bot is ready
@bot.event
async def on_ready():
    # sync bot
    await tree.sync()
    print('Bot is ready')

# create command tree for the bot
tree = bot.tree

# define setup command using command tree
@tree.command(name='setup', description='Setup the bot by selecting what channel you want it to talk in, and the '
                                        'temperature of the AI.')
# set default permissions for setup command
@app_commands.default_permissions(manage_webhooks=True)
# function for setup command
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, temperature: float):

    # check the temperature is between 0 and 2
    if 0 <= temperature <= 2:
        # send message with specified channel and temperature
        await interaction.response.send_message(f'Bot will now talk in {channel} with a temperature of {temperature}')

        # connect to database
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        # check if the server already has a row in the database

        # if the server already has a row in the database

        # if the server does not have a row in the database
        cursor.execute(f'INSERT INTO main VALUES ({interaction.guild.id}, {channel.id}, {temperature})')

    else:
        # send error message
        await interaction.response.send_message('Temperature must be between 0 and 2')

# define help command using command tree
@tree.command(name='help', description='Help command')
# function for help command
async def help(interaction: discord.Interaction):
    # send message with list of commands
    await interaction.response.send_message('Commands:\n/setup <channel> <temperature>,\n/help')

# event handler for when a message is received in the Discord server
@bot.event
async def on_message(message):
    # store message content in prompt variable
    prompt = message.content

    # return if the message was sent by the bot, starts with '!', or was not sent in the specified channel
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        return
    if message.channel.id != bot.chan:
        print('Not correct channel')
        return

    # generate response from OpenAI API
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=bot.temp
    )

    # send response to Discord channel
    await message.channel.send(completion.choices[0].text)
    # process commands in the message
    await bot.process_commands(message)
    print(completion)

# run the bot using the Discord bot token
bot.run(os.getenv('TOKEN'))
