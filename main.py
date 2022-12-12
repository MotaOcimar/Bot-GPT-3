import discord
from discord.ext import commands
from utils import *

# Cria o bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global openai_client
    openai_client = OpenAI(bot.user.name, bot)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.channel.send("pong")

@bot.command()
async def say(ctx, *, arg=None):
    if arg is None:
        return
    await ctx.send(openai_client.say_as_user(ctx.author.name, arg))

@bot.command()
async def act(ctx, *, arg=None):
    if arg is None:
        return
    await ctx.send(openai_client.act_as_user(ctx.author.name, arg))

@bot.command()
async def context(ctx, *, arg=None):
    if arg is None:
        return
    await ctx.send(openai_client.contextualize(arg))

@bot.command()
async def memorize(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Você precisa me dizer o que você quer que eu memorize!")
        return
    openai_client.add_to_memory(arg)
    await ctx.send('Ok, vou me lembrar disso!\n Aqui estão as minhas memórias mais importantes: \n' + openai_client.memories_str())

@bot.command()
async def memories(ctx):
    await ctx.send("Aqui estão as minhas memórias mais importantes:\n" + openai_client.memories_str())

@bot.command()
async def forget(ctx, arg=None):
    if arg is None:
        await ctx.send("Você precisa me dizer qual o númeor da memória você quer que eu esqueça!")
        return
    
    openai_client.remove_memory(int(arg))
    await ctx.send('Ok, esqueci isso!\n Aqui as memórias que me restaram: \n' + openai_client.memories_str())

@bot.command()
async def clear(ctx, arg=None):
    if arg == 'history':
        openai_client.clear_history()
        await ctx.send('Sobre o que a gente tava conversando mesmo?\n Acho que esqueci...')
    elif arg == 'memory':
        openai_client.clear_memory()
        await ctx.send('Ãn!?\n Onde estamos?\nQuem sou eu mesmo?\n Hmm... Tudo bem, ainda lembro do que conversamos!')
    else:
        await ctx.send('Não entendi o que você queria limpar...')


# Carrega o token do arquivo keys/discord.txt
bot.run(open("keys/discord.txt").read())
