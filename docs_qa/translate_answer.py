import os
from openai import AzureOpenAI
import pprint


pp = pprint.PrettyPrinter(indent=2)

llmClient = AzureOpenAI(
    azure_endpoint = os.environ['OPENAI_API_URL_ALTINN3_DEV'],
    api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV'],
    api_version = os.environ['AZURE_OPENAI_VERSION']
)

async def translate_to_language(text_to_translate, target_language_name) -> str:    
    query_result = llmClient.chat.completions.create(
        model=os.environ['AZURE_OPENAI_DEPLOYMENT'],
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
    return query_result.choices[0].message.content
