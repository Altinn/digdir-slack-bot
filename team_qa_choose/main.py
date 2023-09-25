import box
import timeit
import yaml
import asyncio
import pprint
from .run_chain import run_team_query

pp = pprint.PrettyPrinter(indent=2)

async def team_query(user_input):
    return await run_team_query(user_input)


def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(team_query(user_input))
    end = timeit.default_timer()

    answer = response["text"]

    print(f'\nAnswer:\n{answer}')
    print('='*50)

    print(f"Time to retrieve response: {end - start} seconds")
