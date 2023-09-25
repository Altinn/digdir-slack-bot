import os
from os.path import exists
import argparse
from ask_openai import ask_openai

def update_code_summary(prompt: str, codepath: str) -> str:
    """
    Call ask_openai using 'prompt' as system prompt and the contents of 'filepath' as user input.

    Parameters:
    - prompt (str): The system prompt to the assistant.
    - codepath (str): Path to code file to send as user's prompt to the assistant.

    Returns:
    - str: The assistant's reply.
    """    

    with open(codepath, 'r') as codefile:
        user_input = codefile.read()
    
    response = ask_openai(prompt, user_input)

    with open(codepath + ".summary.txt", 'wt') as outputfile:
        outputfile.write(response)

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a list of files and produce code summaries saved to disk.")
    parser.add_argument("pathsfile", help="Filename containing list of code filepaths")    
    parser.add_argument("prompt", help="Name of the file containing the system prompt.")
    args = parser.parse_args()

    with open(args.pathsfile, 'r') as file:
        filepaths = file.read().splitlines()

    with open(args.prompt, 'r') as sysfile:
        system_input = sysfile.read()

    print(f'Prompt: {system_input}')

    for filepath in filepaths:
        if (exists(filepath)):
            print(f'Updating summary for {filepath}')
            response = update_code_summary(system_input, filepath)        
            print(f"{response}")


