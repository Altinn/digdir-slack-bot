import os
from typing import Any, Dict
import pprint
from utils.general import env_var
from utils.llm_utils import azure_client, openai_client, chat_stream

azureClient = azure_client()
openaiClient = openai_client()
pp = pprint.PrettyPrinter(indent=2)

async def translate_to_language(text_to_translate, target_language_name, stream_callback) -> str:    
  query_result = None

  messages: list[Dict[str, Any]]=[
              {
                "role": "system", 
                "content": "You are ChatGPT, a helpful assistant."
              },
              {
                "role": "user", 
                "content": f"Please translate the following to \"{target_language_name}\":\n\n" + text_to_translate
              }
          ]

  if callable(stream_callback):
      translated_answer = chat_stream(messages, stream_callback)
  else:   
    if env_var('USE_AZURE_OPENAI_API') == True:
      query_result = azureClient.chat.completions.create(
          model=env_var('AZURE_OPENAI_DEPLOYMENT'),
          temperature=0.1,
          messages=messages)
    else:
      query_result = openaiClient.chat.completions.create(
          model=env_var('OPENAI_API_MODEL_NAME'),
          temperature=0.1,
          max_retries=0,
          messages=messages)
      
    translated_answer = query_result.choices[0].message.content
  
  return translated_answer
