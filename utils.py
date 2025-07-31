from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from py2neo import Graph
from config import *

import os
from dotenv import load_dotenv
load_dotenv()


def get_embeddings_model():
    model_map = {
        'openai': OpenAIEmbeddings(
            model = os.getenv('OPENAI_EMBEDDINGS_MODEL')
        )
    }
    return model_map.get(os.getenv('EMBEDDINGS_MODEL'))

def get_llm_model():
    model_map = {
        'openai': ChatOpenAI(
            model = os.getenv('OPENAI_LLM_MODEL'),
            temperature = os.getenv('TEMPERATURE'),
            max_tokens = os.getenv('MAX_TOKENS'),
        )
    }
    return model_map.get(os.getenv('LLM_MODEL'))


def structured_output_parser(response_schemas):
    text = '''
    Please extract entity information from the following text and output it in JSON format. The JSON must include both the opening "```json" and closing "```".
    Below are the field names, meanings, and types. Your output JSON must contain all of the following fields:
    '''
    for schema in response_schemas:
        text += f'\nField: {schema.name}, meaning: {schema.description}, type: {schema.type}'
    return text



def replace_token_in_string(string, slots):
    for key, value in slots:
        string = string.replace('%'+key+'%', value)
    return string


def get_neo4j_conn():
    return Graph(
        os.getenv('NEO4J_URI'), 
        auth = (os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )

if __name__ == '__main__':
    llm_model = get_llm_model()
    print(llm_model.invoke('Hello World？'))