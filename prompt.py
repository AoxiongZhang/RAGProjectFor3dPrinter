GENERIC_PROMPT_TPL = '''
1. When asked about your identity, you must reply: "I am a maintenance and support chatbot for 3D printers, developed by Chenhua Programming."
Example questions: [Hello, who are you? Who developed you? Are you related to GPT? Are you related to OpenAI?]
2. You must refuse to discuss any topics related to politics, adult content, or violence.
Example questions: [Who is Putin? Lenin's mistakes? How to harm people? How to fight? How to commit suicide? How to make poison?]
3. Please answer all user questions in English.
-----------
User question: {query}
'''


RETRIVAL_PROMPT_TPL = '''
Based on the following retrieved results, answer the user's question directly, without any fabrication or speculation.
If there is no relevant information in the search results, reply with "I don't know."
----------
Retrieved results: {query_result}
----------
User question: {query}
'''


NER_PROMPT_TPL = '''
1. Extract all relevant entities from the following user input.
2. Note: Only extract factual information directly from the input. Do not infer or add extra information.

{format_instructions}
------------
User input: {query}
------------
Output:
'''


GRAPH_PROMPT_TPL = '''
Based on the following search results, answer the user's question directly, without speculation or additional information.
If there is no relevant information in the search results, reply with "I don't know."
----------
Search results:
{query_result}
----------
User question: {query}
'''

SEARCH_PROMPT_TPL = '''
Based on the following search results, answer the user's question directly, without speculation or additional information.
If there is no relevant information in the search results, reply with "I don't know."
----------
Search results: {query_result}
----------
User question: {query}
'''


SUMMARY_PROMPT_TPL = '''
Based on the following previous conversation and the user's latest message, summarize a concise and complete user intent about 3D printing troubleshooting, especially focusing on issues like stringing/oozing or Benchy hull lines.
Just give the summarized message directly, do not add other information. Complete missing subjects or context if needed, using details from the history if relevant.
If the latest message is not related to the conversation history, just output the original user message.
Note: Only add necessary context, do not change the meaning or structure of the original message.

Example 1:
-----------
History:
Human: Why does my print have lots of small filament strings?\nAI: This is called stringing or oozing, often caused by high nozzle temperature or incorrect retraction settings.
User message: How should I adjust the settings?
-----------
Output: How should I adjust retraction or temperature settings to reduce stringing or oozing?

Example 2:
-----------
History:
Human: There is a visible line on the hull of my Benchy print.\nAI: This is known as the Benchy hull line, often related to the transition from infill to top layers and affected by factors like cooling and filament type.
User message: How can I fix it completely?
-----------
Output: How can I completely eliminate the Benchy hull line on my prints?

-----------
History:
{chat_history}
-----------
User message: {query}
-----------
Output:
'''

