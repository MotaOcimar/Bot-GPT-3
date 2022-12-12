import openai

event_prefix = "<event "
event_suffix = "</event>"

# Events types
SPEECH = "speech"
ACTION = "action"
CONTEXT = "context"

class OpenAI:

    def __init__(self, name, chat_name):
        # Obtem a chave de acesso da OpenAI do arquivo key.json
        openai.api_key = open("keys/openai.txt").read()

        self.history = ""
        self.memories = []
        self.name = name
        self.chat_name = chat_name

    def memories_str(self):
        # retorna uma string com as memórias numeradas e separadas por quebra de linha
        # O índice da memória começa em 1
        return "\n".join([f"[{i+1}] {m}" for i, m in enumerate(self.memories)])

    def call_openai(self, prompt):
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

    def new_event(self, event_type, prompt, user=None):

        user_attr = ""
        if user is not None:
            user_attr = f' user_name="{user}"'

        prompt = f'{event_prefix}type="{event_type}"{user_attr}>{prompt}{event_suffix}\n{event_prefix}type="{SPEECH}" user_name="{self.name}">'
        
        self.history += prompt

        # Chama a OpenAI para completar o texto
        completed_text = self.call_openai(self.memories_str() + "\n\n" + self.history)

        self.history += completed_text + event_suffix + "\n"

        # Printa as memórias e o histórico	
        print(f"{self.memories_str()}\n\n{self.history}")

        return completed_text


    def act_as_user(self, user, prompt):
        return self.new_event(ACTION, prompt, user)
    
    def say_as_user(self, user, prompt):
        return self.new_event(SPEECH, prompt, user)

    def contextualize(self, prompt):
        return self.new_event(CONTEXT, prompt)

    def add_to_memory(self, prompt):
        memories = prompt.split("\n")
        self.memories += memories

    def remove_memory(self, index):
        index -= 1
        self.memories.pop(index)
    
    def clear_memory(self):
        self.memories = []
    
    def clear_history(self):
        self.history = ""
