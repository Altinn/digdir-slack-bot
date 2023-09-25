import box
import timeit
import yaml
import asyncio
import pprint
from .run_chain import run_chain_async

pp = pprint.PrettyPrinter(indent=2)


def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(run_chain_async(user_input))
    end = timeit.default_timer()

    answer = response["text"]

    print(f'\nAnswer:\n{answer}')
    print('='*50)

    print(f"Time to retrieve response: {end - start} seconds")
