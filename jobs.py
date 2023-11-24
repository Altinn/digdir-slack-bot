import asyncio
import argparse
from docs_qa import generate_search_phrases

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('job',
                        type=str,
                        default='',
                        help='Specify a job name - "generate_search_phrases", "sync_github_issues"')
    args = parser.parse_args()

    if args.job == 'generate_search_phrases':
        asyncio.run(generate_search_phrases.run())
