import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import *
import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
is_mutted = False

# Define a função que será chamada quando o comando "/start" for recebido
def start(update, context):
    update.message.reply_text('Olá! Fale comigo o que quiser!')

def callback(update, context):
    # Evita processar mensagens de comandos
    if is_mutted or update.message.text.startswith("/"):
        return
    
    update.message.reply_text(openai_client.say_as_user(update.message.from_user.username, update.message.text))

def mute(update, context):
    global is_mutted
    is_mutted = True
    update.message.reply_text("Escutarei apenas comandos agora")

def unmute(update, context):
    global is_mutted
    is_mutted = False
    update.message.reply_text("Escutarei tudo agora")

def say(update, context, complete=True):
    if len(context.args) == 0:
        return

    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1]
    
    response = openai_client.say_as_user(update.message.from_user.username, arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def act(update, context, complete=True):
    if len(context.args) == 0:
        return

    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1]

    response = openai_client.act_as_user(update.message.from_user.username, arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def do(update, context, complete=True):
    """
    Alias for act
    """
    act(update, context, complete=complete)

def env(update, context, complete=True):
    if len(context.args) == 0:
        return

    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1]

    response = openai_client.env_happen(arg, complete=complete)
    if complete:
        update.message.reply_text(response)

def just(update, context):
    if len(context.args) == 0:
        return
    
    if context.args[0] == "say":
        context.args.pop(0)
        say(update, context, complete=False)
    elif context.args[0] == "act" or context.args[0] == "do":
        context.args.pop(0)
        act(update, context, complete=False)
    elif context.args[0] == "env":
        context.args.pop(0)
        env(update, context, complete=False)
    else:
        update.message.reply_text("Não entendi o que você queria que eu fizesse!")

def poke(update, context):
    update.message.reply_text(openai_client.poke())


def rule(update, context):
    """
    The firs word can be "new", "list" or "del"
    """

    # get the args keeping the formatting
    arg = update.message.text.split(" ", 1)[1]

    if context.args[0] == "new":
        # Remove "new" from args
        context.args.pop(0)
        arg = arg.split(" ", 1)[1]

        # Check if arg is empty
        if len(context.args) == 0:
            update.message.reply_text("Você precisa me dizer o que eu devo lembrar como regra!")
            return

        # Add the rule
        openai_client.add_rule(arg)
        update.message.reply_text('Ok, vou me lembrar disso!\nAqui estão as minhas regras bases: \n' + openai_client.rules_str())

    elif context.args[0] == "list":
        if len(openai_client.rules) == 0:
            update.message.reply_text("Não tenho nenhuma regra ainda!")
            return
        
        update.message.reply_text('Aqui estão as minhas regras bases: \n' + openai_client.rules_str())

    elif context.args[0] == "del":
        # Remove "del" from args
        context.args.pop(0)
        arg = arg.split(" ", 1)[1]

        # Check if arg is empty
        if len(context.args) == 0:
            update.message.reply_text("Você precisa me dizer qual o número da regra você quer que eu esqueça!")
            return

        # Check if arg is 'all'
        elif context.args[0] == "all":
            openai_client.clear_rules()
            update.message.reply_text('Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!')
            return

        # Check if arg is a integer
        elif not context.args[0].isnumeric():
            update.message.reply_text("Você precisa me dizer qual o número da regra você quer que eu esqueça!")
            return

        # Check if arg is a valid rule number
        elif int(context.args[0]) > len(openai_client.rules) or int(context.args[0]) < 1:
            update.message.reply_text("O número da regra que você me deu não é válido!")
            return

        # Remove the rule
        openai_client.remove_rule(int(context.args[0]))
        update.message.reply_text('Ok, esqueci isso!\nAqui as regras que me restaram: \n' + openai_client.rules_str())

    # If arg is not valid
    else:
        update.message.reply_text("Não entendi o que você queria que eu fizesse com as regras...")
        return

def clear(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Não entendi o que você queria que eu esquecesse...")
    elif context.args[0] == "history":
        openai_client.clear_history()
        update.message.reply_text('Sobre o que a gente tava conversando mesmo?\nAcho que esqueci...')
    elif context.args[0] == "rules":
        openai_client.clear_rules()
        update.message.reply_text('Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!')
    else:
        update.message.reply_text("Não entendi o que você queria que eu esquecesse...")
        


def main():
    # Obtenha o token de acesso do seu bot do BotFather
    TOKEN = open("keys/telegram.txt").read()

    # Create the openai client
    global openai_client
    bot = telegram.Bot(token=TOKEN)
    openai_client = OpenAIBot(bot.get_me().username)

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
    dp.add_handler(MessageHandler(Filters.text, callback))


    # Inicie o loop de atualização
    updater.start_polling()

    # Execute até que o usuário pressione Ctrl-C ou o processo seja interrompido
    updater.idle()

if __name__ == '__main__':
    main()
