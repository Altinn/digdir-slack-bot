import os
import pprint
from .config import env_var, azure_client, openai_client

azureClient = azure_client()
openaiClient = openai_client()
pp = pprint.PrettyPrinter(indent=2)

async def translate_to_language(text_to_translate, target_language_name) -> str:    
    query_result = None

    if env_var('USE_AZURE_OPENAI_API') == True:
      query_result = azureClient.chat.completions.create(
          model=env_var('AZURE_OPENAI_DEPLOYMENT'),
          temperature=0.1,
          messages=[
              {
                "role": "system", 
                "content": "You are ChatGPT, a helpful assistant."
              },
              {
                "role": "user", 
                "content": f"Please translate the following to \"{target_language_name}\":\n\n" + text_to_translate
              }
          ])
    else:
      query_result = openaiClient.chat.completions.create(
          model=env_var('OPENAI_API_MODEL_NAME'),
          temperature=0.1,
          max_retries=0,
          messages=[
              {
                "role": "system", 
                "content": "You are ChatGPT, a helpful assistant."
              },
              {
                "role": "user", 
                "content": f"Please translate the following to \"{target_language_name}\":\n\n" + text_to_translate
              }
          ])
    
    # Extract and return the assistant's reply
    return query_result.choices[0].message.content
