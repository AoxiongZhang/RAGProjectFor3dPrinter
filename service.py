from prompt import *
from utils import *
from agent import *

from langchain.chains import LLMChain
from langchain.prompts import Prompt

class Service():
    def __init__(self):
        self.agent = Agent()

    def get_summary_message(self, message, history):
        llm = get_llm_model()
        prompt = Prompt.from_template(SUMMARY_PROMPT_TPL)
        llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=os.getenv('VERBOSE'))
        chat_history = ''
        # Extract last two user-assistant pairs
        qa_pairs = []
        i = 0
        while i < len(history) - 1:
            if history[i]['role'] == 'user' and history[i + 1]['role'] == 'assistant':
                qa_pairs.append((history[i]['content'], history[i + 1]['content']))
                i += 2
            else:
                i += 1
        for q, a in qa_pairs[-2:]:
            chat_history += f'User: {q}\nAI: {a}\n'
        return llm_chain.invoke({'query': message, 'chat_history': chat_history})['text']

    def answer(self, message, history):
        if history:
            message = self.get_summary_message(message, history)
        return self.agent.query(message)


if __name__ == '__main__':
    service = Service()
    # Example: user history from 3D printing troubleshooting scenarios
    print(service.answer('How can I get rid of the Benchy hull line?', [
        ['Why does my Benchy print have a visible line on the hull?', 'This is known as the Benchy hull line, and it often occurs due to the transition from infill to top layers, affected by factors like cooling and filament type.'],
        ['What causes stringing or oozing?', 'Stringing or oozing is usually caused by excessive nozzle temperature or improper retraction settings.'],
    ]))