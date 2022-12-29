import discord
from discord.ext import commands
from openai_bot.api import OpenAIBot

# Cria o bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
is_mutted = False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global api
    api = OpenAIBot(bot.user)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if is_mutted or message.content.startswith("/"):
        await bot.process_commands(message)
        return

    response = api.on_message(message.author, message.content)
    await message.channel.send(response)

@bot.command()
async def mute(ctx):
    global is_mutted
    is_mutted = True
    await ctx.channel.send(api.mute())

@bot.command()
async def unmute(ctx):
    global is_mutted
    is_mutted = False
    await ctx.channel.send(api.unmute())

@bot.command()
async def hello(ctx):
    await ctx.channel.send(f"hello {ctx.author}!")

@bot.command()
async def say(ctx, *, arg=None, complete=True):
    response  = api.say(ctx.author, arg, complete=complete)
    if complete:
        await ctx.send(response)

@bot.command()
async def act(ctx, *, arg=None, complete=True):
    response  = api.act(ctx.author, arg, complete=complete)
    if complete:
        await ctx.send(response)

@bot.command()
async def do(ctx, *, arg=None, complete=True):
    """
    act alias
    """
    await act(ctx, arg=arg, complete=complete)

@bot.command()
async def env(ctx, *, arg=None, complete=True):
    response  = api.env(arg, complete=complete)
    if complete:
        await ctx.send(response)

@bot.command()
async def just(ctx, *, arg=None):
    response = api.just(ctx.author, arg)
    if response is None or response == "":
        return
    await ctx.send(response)

@bot.command()
async def poke(ctx, arg=None):
    await ctx.send(api.poke())

@bot.command()
async def rule(ctx, *, arg=None):
    await ctx.send(api.rule(arg))

@bot.command()
async def clear(ctx, arg=None):
    await ctx.send(api.clear(arg))

# Carrega o token do arquivo keys/discord.txt
bot.run(open("keys/discord.txt").read())
