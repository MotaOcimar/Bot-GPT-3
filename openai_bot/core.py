import openai

event_prefix = "<event "
event_suffix = "</event>"

# Events types
SPEECH = "speech"
ACTION = "action"
ENV_EVENT = "environment"

class OpenAIBotCore:

    def __init__(self, botName):
        # Obtem a chave de acesso da OpenAI do arquivo key.json
        openai.api_key = open("keys/openai.txt").read()

        self.__history = ""
        self.__rules = []
        self.__name = botName

    def __rules_str(self):
        # retorna uma string com as regras numeradas e separadas por quebra de linha
        # O índice da regra começa em 1
        return "\n".join([f"[{i+1}] {m}" for i, m in enumerate(self.__rules)])

    def __full_prompt(self):
        # Retorna o prompt completo para a OpenAI
        return self.__rules_str() + "\n\n" + self.__history

    def __call_openai(self, prompt):
        # Cria um modelo de completação usando o GPT-3 da OpenAI
        completion_model = openai.Completion.create(
            engine="text-davinci-003",
            prompt= prompt,
            temperature=0.7,
            max_tokens=256,
            stop=[event_prefix, event_suffix]
        )

        # Obtem a sugestão de completamento do texto
        completed_text = completion_model["choices"][0]["text"]

        if completed_text == "":
            completed_text = "..."

        return completed_text

    def __get_response(self):
        self.__history += f'{event_prefix}type="{SPEECH}" username="{self.__name}">'

        # Chama a OpenAI para completar o texto
        completed_text = self.__call_openai(self.__full_prompt())

        self.__history += completed_text + event_suffix + "\n"

        # Printa as regras e o histórico	
        print(f"{self.__full_prompt()}")

        return completed_text

    def __new_event(self, event_type, prompt, user=None, complete=True):

        user_attr = ""
        if user is not None:
            user_attr = f' username="{user}"'

        prompt = f'{event_prefix}type="{event_type}"{user_attr}>{prompt}{event_suffix}\n'
        self.__history += prompt
        
        if not complete:
            # Printa as regras e o histórico	
            print(f"{self.__rules_str()}\n\n{self.__history}")
            return ''

        return self.__get_response()

    def __user_acts(self, user, prompt, complete=True):
        return self.__new_event(ACTION, prompt, user, complete)
    
    def __user_says(self, user, prompt, complete=True):
        return self.__new_event(SPEECH, prompt, user, complete)

    def __env_happen(self, prompt, complete=True):
        return self.__new_event(ENV_EVENT, prompt, complete=complete)

    def __poke(self):
        return self.__get_response()

    def __add_rule(self, prompt):
        rules = prompt.split("\n")
        self.__rules += rules

    def __remove_rule(self, index):
        index -= 1
        self.__rules.pop(index)
    
    def __clear_rules(self):
        self.__rules = []
    
    def __clear_history(self):
        self.__history = ""
