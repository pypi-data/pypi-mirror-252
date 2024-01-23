import re
import openai
from IPython.core.magic import register_cell_magic
from IPython.display import display, Code
from IPython.core.display import Markdown
from IPython.core.getipython import get_ipython


def getChatResponse(question):
    params = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": question 
                }],
            "temperature": 0.2,
            "n": 1,
            "stop": [ " Human:", " AI:" ]
            }
    response = openai.ChatCompletion.create(**params) 
    return response.choices[0].message.content


@register_cell_magic
def chat(line, cell):
    OPENAI_API_KEY = line.strip()
    question = cell.strip()
    if not OPENAI_API_KEY:
        print("Please provide OPENAI_API_KEY")
        return
    openai.api_key = OPENAI_API_KEY
    if not question:
        print("Please provide question")
        return
    response = getChatResponse(question)
    code_blocks = re.findall(r'```(.*?)```', response, re.DOTALL)
    text_data = re.sub(r'```.*?```', '', response, flags=re.DOTALL)

    if text_data:
        display(Markdown(text_data))

    if code_blocks:
        code_cell = '\n\n'.join(code_blocks)
        display(Code(code_cell))


def load_ipython_extension(ipython):
    ipython.register_magic_function(chat)
load_ipython_extension(get_ipython())
