import asyncio
import argparse
from docs_qa import generate_search_phrases
from github_qa.sync_issues import main as sync_issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('job',
                        type=str,
                        default='',
                        help='Specify a job name - "generate_search_phrases", "sync_github_issues"')
    parser.add_argument('param1',
                        nargs='?',
                        default=None,
                        type=str,
                            help='Specify a parameter')
    args = parser.parse_args()

    if args.job == 'generate_search_phrases':
        asyncio.run(generate_search_phrases.run(args.param1))

    elif args.job == 'sync_github_issues':
        sync_issues()

    else:
        print(f'Unknown job name "{args.job}"')
