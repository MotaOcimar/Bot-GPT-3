import discord
from utils import *

# Cria o bot
intents = discord.Intents.all()
client = discord.Client(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global openai_client
    openai_client = OpenAI(client.user.name, client)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Message from {message.author}: {message.content}")

    if message.content.startswith('/say '):
        await message.channel.send(openai_client.say_as_user(message.author.name, message.content.replace('/say ', '')))

    if message.content.startswith('/act '):
        await message.channel.send(openai_client.act_as_user(message.author.name, message.content.replace('/act ', '')))
    
    if message.content.startswith('/context '):
        await message.channel.send(openai_client.contextualize(message.content.replace('/context ', '')))

    if message.content.startswith('/clear history'):
        openai_client.clear_history()
        await message.channel.send('Sobre o que a gente tava conversando mesmo?\n Acho que esqueci...')

    if message.content.startswith('/clear memory'):
        openai_client.clear_memory()
        await message.channel.send('Ãn!?\n Onde estamos?\nQuem sou eu mesmo?\n Hmm... Tudo bem, ainda lembro do que conversamos!')

    if message.content.startswith('/memorize '):
        openai_client.add_to_memory(message.content.replace('/memorize ', ''))
        await message.channel.send('Ok, vou me lembrar disso!\n Aqui estão as minhas memórias mais importantes: \n' + openai_client.memories_str())

    if message.content.startswith('/memories'):
        await message.channel.send("Aqui estão as minhas memórias mais importantes:\n" + openai_client.memories_str())

    if message.content.startswith('/forget '):
        openai_client.remove_memory(int(message.content.replace('/forget ', '')))
        await message.channel.send('Ok, esqueci isso!\n Aqui as memórias que me restaram: \n' + openai_client.memories_str())   


# Carrega o token do arquivo keys/discord.txt
client.run(open("keys/discord.txt").read())
