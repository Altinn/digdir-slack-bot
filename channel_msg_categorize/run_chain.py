import box
import timeit
import yaml
import asyncio
import pprint
from .build_chain import setup_dbqa
from dto.llm_response import LLMResponse
from .config_chain import config

pp = pprint.PrettyPrinter(indent=2)

cfg = config()

dbqa = setup_dbqa()
    

async def run_chain_async(user_input):
    print(f'user_input:', user_input)

    start = timeit.default_timer()
    response = dbqa(user_input)
    end = timeit.default_timer()
    response['duration'] = end - start

    return response


def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(run_chain_async(user_input))
    
    answer = response["text"]

    print(f'\nAnswer:\n{answer}')
    print('='*50)

    print(f"Time to retrieve response: {end - start} seconds")
