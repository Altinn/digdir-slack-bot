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
    #     start = timeit.default_timer()
#     response = await team_query(user_input)
#     end = timeit.default_timer()
#     print('-- incoming_message_category - raw llm response --')
#     pp.pprint(response)
#     answer = response.get('text', 'No answer found')  # Use get method to avoid KeyError
#     return answer, round(end - start)

    print(f'user_input:', user_input)
    response = dbqa(user_input)
    return response


def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(run_chain_async(user_input))
    end = timeit.default_timer()

    answer = response["text"]

    print(f'\nAnswer:\n{answer}')
    print('='*50)

    print(f"Time to retrieve response: {end - start} seconds")
