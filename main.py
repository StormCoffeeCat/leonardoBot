# imports
import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

# openai setup
openai.organization = os.getenv('ORG')
openai.api_key = os.getenv('KEY')

# discord setup
bot = commands.Bot(command_prefix='./', intents=discord.Intents.all(), help_command=None)

# variable setup
bot.chan = 'str'
bot.temp = 0.5


@bot.event
async def on_ready():
    await tree.sync()
    print('Bot is ready')


tree = bot.tree


# define your commands using the @tree.command decorator
@tree.command(name='ping', description='Pong!')
async def ping(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f'Pong! {message}')
    print(message)


@tree.command(name='setup', description='Setup the bot by selecting what channel you want it to talk in, and the '
                                        'temperature of the AI.')
@app_commands.default_permissions(manage_webhooks=True)
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, temperature: float):
    await interaction.response.send_message(f'Bot will now talk in {channel} with a temperature of {temperature}')

    bot.chan = channel.id
    bot.temp = temperature

    async def setup(interaction: discord.Interaction):
        await interaction.response.send_message('You do not have permission to use this command')


@tree.command(name='help', description='Help command')
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f'Commands: /ping <message>, /setup <channel> <temperature>, /help')

# bot checks for message
@bot.event
async def on_message(message):
    prompt = message.content

    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        return
    if message.channel.id != bot.chan:
        print('Not correct channel')
        return

    # prompts the ai to generate a response
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=bot.temp
    )

    # sends the response to the channel
    await message.channel.send(completion.choices[0].text)
    await bot.process_commands(message)
    print(completion)


# run bot
bot.run(os.getenv('TOKEN'))
