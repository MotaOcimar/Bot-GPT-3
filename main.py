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
    openai_client = OpenAIBot(bot.user)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.channel.send(f"hello {ctx.author}!")

@bot.command()
async def say(ctx, *, arg=None, complete=True):
    if arg is None:
        return

    response  = openai_client.say_as_user(ctx.author, arg, complete=complete)
    if complete:
        await ctx.send(response)
        return

@bot.command()
async def act(ctx, *, arg=None, complete=True):
    if arg is None:
        return

    response  = openai_client.act_as_user(ctx.author, arg, complete=complete)
    if complete:
        await ctx.send(response)
        return

@bot.command()
async def do(ctx, *, arg=None, complete=True):
    """
    act alias
    """
    await act(ctx, arg=arg, complete=complete)

@bot.command()
async def env(ctx, *, arg=None, complete=True):
    if arg is None:
        return

    response  = openai_client.env_happen(arg, complete=complete)
    if complete:
        await ctx.send(response)
        return

@bot.command()
async def just(ctx, *, arg=None):
    # Check if arg is empty
    if arg is None:
        return
    
    # Check if arg start with "say"
    if arg.startswith("say"):
        # Remove the first word
        arg = arg.split(" ", 1)[1]
        await say(ctx, arg=arg, complete=False)
    
    # Check if arg start with "act"
    elif arg.startswith("act") or arg.startswith("do"):
        # Remove the first word
        arg = arg.split(" ", 1)[1]
        await act(ctx, arg=arg, complete=False)

    # Check if arg start with "env"
    elif arg.startswith("env"):
        # Remove the first word
        arg = arg.split(" ", 1)[1]
        await env(ctx, arg=arg, complete=False)
    
    # If arg is not valid
    else:
        await ctx.send("Não entendi o que você queria que eu fizesse!")

@bot.command()
async def poke(ctx, arg=None):
    await ctx.send(openai_client.poke())


@bot.command()
async def rule(ctx, *, arg=None):
    """
    The first word can be "new", "list" or "del"
    """

    # Check if arg start with "new"
    if arg.startswith("new"):
        # Remove the first word
        arg = arg.split(" ", 1)[1]

        # Check if arg is empty
        if arg is None:
            await ctx.send("Você precisa me dizer o que eu devo lembrar como regra!")
            return
        
        # Add the rule
        openai_client.add_rule(arg)
        await ctx.send('Ok, vou me lembrar disso!\n Aqui estão as minhas regras bases: \n' + openai_client.rules_str())

    # Check if arg start with "list"
    elif arg.startswith("list"):
        if len(openai_client.rules) == 0:
            await ctx.send("Não tenho nenhuma regra ainda!")
            return
        
        await ctx.send("Aqui estão as minhas regras bases:\n" + openai_client.rules_str())

    # Check if arg start with "del"
    elif arg.startswith("del"):
        # Remove the first word
        arg = arg.split(" ", 1)[1]

        # Check if arg is empty
        if arg is None:
            await ctx.send("Você precisa me dizer qual o número da regra você quer que eu esqueça!")
            return

        # Check if arg is 'all'
        elif arg == 'all':
            openai_client.clear_rules()
            await ctx.send('Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!')
            return
        
        # Check if arg is a integer
        elif not arg.isnumeric():
            await ctx.send("Você precisa me dizer qual o número da regra você quer que eu esqueça!")
            return

        # Check if arg is a valid rule number
        elif int(arg) > len(openai_client.rules) or int(arg) < 1:
            await ctx.send("O número da regra que você me deu não é válido!")
            return

        # Remove the rule        
        openai_client.remove_rule(int(arg))
        await ctx.send('Ok, esqueci isso!\n Aqui as regras que me restaram: \n' + openai_client.rules_str())
    
    # If arg is not valid
    else:
        await ctx.send("Não entendi o que você queria que eu fizesse com as regras...")
        return


@bot.command()
async def clear(ctx, arg=None):
    if arg == 'history':
        openai_client.clear_history()
        await ctx.send('Sobre o que a gente tava conversando mesmo?\n Acho que esqueci...')
    elif arg == 'rules':
        openai_client.clear_rules()
        await ctx.send('Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!')
    else:
        await ctx.send('Não entendi o que você queria limpar...')


# Carrega o token do arquivo keys/discord.txt
bot.run(open("keys/discord.txt").read())
