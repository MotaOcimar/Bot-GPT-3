from openai_bot.core import OpenAIBotCore


class OpenAIBot(OpenAIBotCore):
    def __init__(self, botName):
        super().__init__(botName)

    def on_message(self, author, content):
            return self._OpenAIBotCore__user_says(author, content)

    def mute(self):
        return "Escutarei apenas comandos agora"

    def unmute(self):
        return "Escutarei tudo agora"

    def say(self, author, arg=None, complete=True):
        if arg is None:
            return "Diga algo para eu responder"

        return self._OpenAIBotCore__user_says(author, arg, complete=complete)

    def act(self, author, arg=None, complete=True):
        if arg is None:
            return "Diga uma ação que para encenar"

        return self._OpenAIBotCore__user_acts(author, arg, complete=complete)

    def env(self, arg=None, complete=True):
        if arg is None:
            return "Diga algo que aconteceu no ambiente ao nosso redor"

        return self._OpenAIBotCore__env_happen(arg, complete=complete)

    def just(self, author, arg=None):
        if arg is None:
            return "Apenas o que? Use 'just say', 'just act' ou 'just env'"
        
        if arg.startswith("say"):
            # Remove the first word
            arg = arg.split(" ", 1)[1]
            self.say(author, arg=arg, complete=False)
            return None
        elif arg.startswith("act") or arg.startswith("do"):
            # Remove the first word
            arg = arg.split(" ", 1)[1]
            self.act(author, arg=arg, complete=False)
            return None
        elif arg.startswith("env"):
            # Remove the first word
            arg = arg.split(" ", 1)[1]
            self.env(arg=arg, complete=False)
            return None
        else:
            return "Não entendi o que você queria que eu fizesse!"

    def poke(self):
        return self._OpenAIBotCore__poke()

    def rule(self, arg=None):
        if arg.startswith("new"):
            # Remove the first word
            arg = arg.split(" ", 1)[1]

            # Check if arg is empty
            if arg is None:
                return "Você precisa me dizer o que eu devo lembrar como regra!"
            
            # Add the rule
            self._OpenAIBotCore__add_rule(arg)
            return 'Ok, vou me lembrar disso!\nAqui estão as minhas regras bases: \n' + self._OpenAIBotCore__rules_str()

        elif arg.startswith("list"):
            if len(self._OpenAIBotCore__rules) == 0:
                return "Não tenho nenhuma regra ainda!"
            
            return "Aqui estão as minhas regras bases:\n" + self._OpenAIBotCore__rules_str()

        elif arg.startswith("del"):
            # Remove the first word
            arg = arg.split(" ", 1)[1]

            # Check if arg is empty
            if arg is None:
                return "Você precisa me dizer qual o número da regra você quer que eu esqueça!"

            # Check if arg is 'all'
            elif arg == 'all':
                self._OpenAIBotCore__clear_rules()
                return 'Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!'
            
            # Check if arg is a integer
            elif not arg.isnumeric():
                return "Você precisa me dizer qual o número da regra você quer que eu esqueça!"

            # Check if arg is a valid rule number
            elif int(arg) > len(self._OpenAIBotCore__rules) or int(arg) < 1:
                return "O número da regra que você me deu não é válido!"

            # Remove the rule        
            self._OpenAIBotCore__remove_rule(int(arg))
            return 'Ok, esqueci isso!\nAqui as regras que me restaram: \n' + self._OpenAIBotCore__rules_str()

        else:
            return "O que devo fazer com as regras? Use 'rule new', 'rule list' ou 'rule del'"

    def clear(self, arg=None):
        if arg == 'history':
            self._OpenAIBotCore__clear_history()
            return 'Sobre o que a gente tava conversando mesmo?\nAcho que esqueci...'
        elif arg == 'rules':
            self._OpenAIBotCore__clear_rules()
            return 'Ãn!?\nOnde estamos?\nQuem sou eu mesmo?\nHmm... Tudo bem, ainda lembro do que conversamos!'
        else:
            return 'Não entendi o que você queria limpar...'
