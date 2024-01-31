import timeit
import pprint
from dataclasses import dataclass
import json
from typing import Any, Dict
from utils.general import env_var
import instructor
from openai import AzureOpenAI, OpenAI

@dataclass
class JsonExtraction:
    json_dict: Dict[str, Any]
    response_json_removed: str


def extract_json_from_response(response: str, json_doc_keyword: str) -> JsonExtraction:
    """
    This function extracts a JSON document from a response string.

    Parameters:
    response (str): The response string containing the JSON document.
    json_doc_keyword (str): The keyword indicating the start of the JSON document.

    Returns:
    JsonExtraction: A dataclass containing the extracted JSON document and the remaining response string.
    """
    
    if json_doc_keyword.lower() in response.lower():
        keyword_start = response.lower().index(json_doc_keyword.lower())
        json_doc_start = keyword_start  + len(json_doc_keyword)
        json_str = response[json_doc_start:].strip()

        # check if json is wrapped in markdown-style code block  ```{ "attribute": "value"}  ```
        if (json_str.startswith('```') 
            and json_str.endswith('```')
            and "\n" in json_str):
            # Remove the markdown-style code block, including code language indicator (```json)
            json_str = json_str[json_str.index("\n"):-3].strip()

        response_json_removed = response[:keyword_start].strip()
        print(f'json_doc:\n{json_str}')

        # Load the JSON string into a Python dictionary
        json_dict = json.loads(json_str)
        return JsonExtraction(json_dict, response_json_removed)
    
    return JsonExtraction({}, response)
             

def azure_client():
    return instructor.patch(AzureOpenAI(
        azure_endpoint = env_var('AZURE_OPENAI_API_URL'),
        api_key = env_var('AZURE_OPENAI_API_KEY'),
        api_version = env_var('AZURE_OPENAI_VERSION'),
        
    ))

def openai_client():
    return instructor.patch(OpenAI(api_key = env_var('OPENAI_API_KEY')))

def chat_stream(messages: list[Dict[str, Any]], callback, callback_interval_seconds=3.0):
    content_so_far = ''
    latest_chunk = ''
    chunk_count = 0
    last_callback = timeit.default_timer()

    if not callable(callback):
        raise Exception("Chat stream callback is not a function.")
    
    llm_client = None

    if env_var('USE_AZURE_OPENAI_API'):
        print(f"chat_stream - azure deployment: {env_var('AZURE_OPENAI_DEPLOYMENT')}")

        llm_client = azure_client()
        for chunk in llm_client.chat.completions.create(
                    model=env_var('AZURE_OPENAI_DEPLOYMENT'),
                    temperature=0.1,
                    max_retries=0,
                    messages=messages,
                    stream=True):
            
            # pprint.pprint(chunk)
            content = chunk.choices[0].delta.content if len(chunk.choices) > 0 else None

            if content is not None:
                latest_chunk += content
                content_so_far += content
                chunk_count += 1

            if timeit.default_timer() - last_callback >= callback_interval_seconds or (len(chunk.choices) > 0 and chunk.choices[0].finish_reason == 'stop'):
                last_callback = timeit.default_timer()        
                callback(latest_chunk)
                latest_chunk = ''

    else:
        print(f"chat_stream - model: {env_var('OPENAI_API_MODEL_NAME')}")
        llm_client = openai_client()
        for chunk in llm_client.chat.completions.create(
                    model=env_var('OPENAI_API_MODEL_NAME'),
                    temperature=0.1,
                    max_retries=0,
                    messages=messages,
                    stream=True):
            
            content = chunk.choices[0].delta.content if len(chunk.choices) > 0 else None

            if content is not None:
                latest_chunk += content                
                content_so_far += content
                chunk_count += 1

            if timeit.default_timer() - last_callback >= callback_interval_seconds or (len(chunk.choices) > 0 and chunk.choices[0].finish_reason == 'stop'):
                last_callback = timeit.default_timer()
                callback(latest_chunk)
                latest_chunk = ''

    return content_so_far

