import argparse
import asyncio
from docs_qa import main as docs_qa_main
from code_qa import main as code_qa_main
from team_qa_choose import main as team_qa_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('botname',
                        type=str,
                        default='docs',
                        help='Specify a bot name - "docs", "team" or "code"')
    parser.add_argument('userinput',
                        type=str,
                        default='test query',
                        help='Specify a query')
    args = parser.parse_args()

    if args.botname == 'docs':
        asyncio.run(docs_qa_main.main(args.userinput))
    elif args.botname == 'code':
        code_qa_main.main(args.userinput)
    elif args.botname == 'team':
        team_qa_main.main(args.userinput)