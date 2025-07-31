from utils import *
from config import *
from prompt import *

import os
from langchain.chains import LLMChain, LLMRequestsChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma, FAISS
from langchain.schema import Document
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain import hub

class Agent():
    def __init__(self):
        self.vdb = Chroma(
            persist_directory=os.path.join(os.path.dirname(__file__), './data/db'),
            embedding_function=get_embeddings_model()
        )

    def generic_func(self, x, query):
        prompt = PromptTemplate.from_template(GENERIC_PROMPT_TPL)
        llm_chain = LLMChain(
            llm=get_llm_model(),
            prompt=prompt,
            verbose=os.getenv('VERBOSE')
        )
        return llm_chain.invoke(query)['text']

    def retrival_func(self, x, query):
        # Retrieve and filter relevant documents
        documents = self.vdb.similarity_search_with_relevance_scores(query, k=5)
        query_result = [doc[0].page_content for doc in documents if doc[1] > 0.7]

        # Fill prompt and summarize the answer
        prompt = PromptTemplate.from_template(RETRIVAL_PROMPT_TPL)
        retrival_chain = LLMChain(
            llm=get_llm_model(),
            prompt=prompt,
            verbose=os.getenv('VERBOSE')
        )
        inputs = {
            'query': query,
            'query_result': '\n\n'.join(query_result) if len(query_result) else 'No results found'
        }
        return retrival_chain.invoke(inputs)['text']

    def graph_func(self, x, query):
        # Named Entity Recognition for 3D printer handbook entities
        response_schemas = [
            ResponseSchema(type='list', name='printer', description='3D printer model or product line'),
            ResponseSchema(type='list', name='error',
                           description='3D printing error or printing defect, such as stringing, oozing, or Benchy hull line'),
            ResponseSchema(type='list', name='cause',
                           description='Possible causes or influencing factors of the error (e.g. high temperature, retraction settings, cooling issues)'),
            ResponseSchema(type='list', name='solution',
                           description='Solution, adjustment, or troubleshooting step to solve the error'),
            ResponseSchema(type='list', name='setting',
                           description='Specific slicer or printer settings, such as retraction distance, retraction speed, temperature, or cooling'),
            ResponseSchema(type='list', name='material',
                           description='Filament or material types used in 3D printing, such as PLA, PETG, ABS'),
            ResponseSchema(type='list', name='part',
                           description='Printer components relevant to the error, such as nozzle, extruder, cooling fan'),
        ]

        output_parser = StructuredOutputParser(response_schemas=response_schemas)
        format_instructions = structured_output_parser(response_schemas)

        ner_prompt = PromptTemplate(
            template=NER_PROMPT_TPL,
            partial_variables={'format_instructions': format_instructions},
            input_variables=['query']
        )

        ner_chain = LLMChain(
            llm=get_llm_model(),
            prompt=ner_prompt,
            verbose=os.getenv('VERBOSE')
        )

        result = ner_chain.invoke({'query': query})['text']
        ner_result = output_parser.parse(result)

        # Fill graph templates with extracted entities
        graph_templates = []
        for key, template in GRAPH_TEMPLATE.items():
            slot = template['slots'][0]
            slot_values = ner_result.get(slot, [])
            for value in slot_values:
                graph_templates.append({
                    'question': replace_token_in_string(template['question'], [[slot, value]]),
                    'cypher': replace_token_in_string(template['cypher'], [[slot, value]]),
                    'answer': replace_token_in_string(template['answer'], [[slot, value]]),
                })
        if not graph_templates:
            return

        # Semantic similarity filtering
        graph_documents = [
            Document(page_content=template['question'], metadata=template)
            for template in graph_templates
        ]
        db = FAISS.from_documents(graph_documents, get_embeddings_model())
        graph_documents_filter = db.similarity_search_with_relevance_scores(query, k=3)

        # Execute Cypher queries on Neo4j and collect answers
        query_result = []
        neo4j_conn = get_neo4j_conn()
        for document in graph_documents_filter:
            question = document[0].page_content
            cypher = document[0].metadata['cypher']
            answer = document[0].metadata['answer']
            try:
                result = neo4j_conn.run(cypher).data()
                if result and any(value for value in result[0].values()):
                    answer_str = replace_token_in_string(answer, list(result[0].items()))
                    query_result.append(f'Question: {question}\nAnswer: {answer_str}')
            except Exception as e:
                pass

        # Summarize final answer using LLM
        prompt = PromptTemplate.from_template(GRAPH_PROMPT_TPL)
        graph_chain = LLMChain(
            llm=get_llm_model(),
            prompt=prompt,
            verbose=os.getenv('VERBOSE')
        )
        inputs = {
            'query': query,
            'query_result': '\n\n'.join(query_result) if len(query_result) else 'No relevant result found'
        }
        return graph_chain.invoke(inputs)['text']

    def search_func(self, query):
        prompt = PromptTemplate.from_template(SEARCH_PROMPT_TPL)
        llm_chain = LLMChain(
            llm=get_llm_model(),
            prompt=prompt,
            verbose=os.getenv('VERBOSE')
        )
        llm_request_chain = LLMRequestsChain(
            llm_chain=llm_chain,
            requests_key='query_result'
        )
        inputs = {
            'query': query,
            'url': 'https://www.google.com/search?q=' + query.replace(' ', '+')
        }
        return llm_request_chain.invoke(inputs)['output']

    def query(self, query):
        tools = [
            Tool.from_function(
                name='generic_func',
                func=lambda x: self.generic_func(x, query),
                description='Answer general knowledge or small talk about the 3D printer.'
            ),
            Tool.from_function(
                name='retrival_func',
                func=lambda x: self.retrival_func(x, query),
                description='Answer handbook-related questions from the vector database.'
            ),
            Tool(
                name='graph_func',
                func=lambda x: self.graph_func(x, query),
                description='Answer entity-relationship or troubleshooting questions using the knowledge graph.'
            ),
            Tool(
                name='search_func',
                func=self.search_func,
                description='Fallback to web search if other tools cannot answer.'
            ),
        ]

        # Use react-style agent with conversation memory
        prompt = hub.pull('hwchase17/react-chat')
        agent = create_react_agent(llm=get_llm_model(), tools=tools, prompt=prompt)
        memory = ConversationBufferMemory(memory_key='chat_history')
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=memory,
            handle_parsing_errors=True,
            verbose=os.getenv('VERBOSE')
        )
        return agent_executor.invoke({"input": query})['output']


if __name__ == '__main__':
    agent = Agent()
    print(agent.query('What materials can Prusa MK4S print?'))
    # Example: print(agent.query('How to solve bed leveling error?'))
