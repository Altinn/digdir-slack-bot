import os
import openai
import pprint

openai.api_type = 'azure'
openai.api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']
openai.api_base = os.environ['OPENAI_API_URL_ALTINN3_DEV']
openai.api_version = os.environ['AZURE_OPENAI_VERSION']

pp = pprint.PrettyPrinter(indent=2)


async def translate_to_language(text_to_translate, target_language_name) -> str:    
    query_result = openai.ChatCompletion.create(
        engine=os.environ['AZURE_OPENAI_DEPLOYMENT'],
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
    
    # Extract and return the assistant's reply
    return query_result.choices[0].message['content']
