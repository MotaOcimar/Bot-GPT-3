import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai_bot.api import OpenAIBot
import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
is_mutted = False

# Define a função que será chamada quando o comando "/start" for recebido
def start(update, context):
    update.message.reply_text('Olá! Fale comigo o que quiser!')

def on_message(update, context):
    # Evita processar mensagens de comandos
    if is_mutted or update.message.text.startswith("/"):
        return

    response = api.on_message(update.message.from_user.username, update.message.text)
    update.message.reply_text(response)

def mute(update, context):
    global is_mutted
    is_mutted = True
    update.message.reply_text(api.mute())

def unmute(update, context):
    global is_mutted
    is_mutted = False
    update.message.reply_text(api.unmute())

def say(update, context, complete=True):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None
    
    response = api.say(update.message.from_user.username, arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def act(update, context, complete=True):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None

    response = api.act(update.message.from_user.username, arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def do(update, context, complete=True):
    """
    Alias for act
    """
    act(update, context, complete=complete)

def env(update, context, complete=True):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None

    response = api.env(arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def just(update, context):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None

    response = api.just(update.message.from_user.username, arg)
    if response is None or response == "":
        return
    update.message.reply_text(response)

def poke(update, context):
    update.message.reply_text(api.poke())

def rule(update, context):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None

    update.message.reply_text(api.rule(arg))

def clear(update, context):
    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1] if len(update.message.text.split(" ")) > 1 else None

    update.message.reply_text(api.clear(arg))

def main():
    # Obtenha o token de acesso do seu bot do BotFather
    TOKEN = open("keys/telegram.txt").read()

    # Create the openai client
    global api
    bot = telegram.Bot(token=TOKEN)
    api = OpenAIBot(bot.get_me().username)

    # Crie um objeto Updater usando o seu token de acesso
    updater = Updater(TOKEN, use_context=True)

    # Obtenha o dispatcher para registrar os manipuladores de comandos
    dp = updater.dispatcher

    # Registre o manipulador de comandos para cada comando
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("unmute", unmute))
    dp.add_handler(CommandHandler("say", say))
    dp.add_handler(CommandHandler("act", act))
    dp.add_handler(CommandHandler("do", do))
    dp.add_handler(CommandHandler("env", env))
    dp.add_handler(CommandHandler("just", just))
    dp.add_handler(CommandHandler("poke", poke))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(MessageHandler(Filters.text, on_message))


    # Inicie o loop de atualização
    updater.start_polling()

    # Execute até que o usuário pressione Ctrl-C ou o processo seja interrompido
    updater.idle()

if __name__ == '__main__':
    main()
