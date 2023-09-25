# New README.md 

## TODO: document db_build for docs_qa and code_qa

### code_qa

produce list of filenames to generate summaries for:
find /Users/<path_to_repos>/altinn/apps/ValidateData -type f | grep "ValidationHandler.cs$" > needs-summary-update.txt

from project root folder:

poetry run python3 code_qa/update_summaries.py <path_to>/needs-summary-update.txt ./code_qa/prompts/altinn3-csharp-code-summarize.txt



## Quickstart
- Check that you have the GGML binary file from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML and placed it into the `models/` folder
- install dependencies:
`poetry install`
- To start the Slack bot endpoint, launch the terminal from the project directory and run the following command:
`poetry run python3 bolt.py`
- For example, `poetry run python3 main.py docs "How can I add a new text field to my data model?"`
<br><br>

___


## Tools
- **LangChain**: Framework for developing applications powered by language models
- **C Transformers**: Python bindings for the Transformer models implemented in C/C++ using GGML library
- **FAISS**: Open-source library for efficient similarity search and clustering of dense vectors.
- **Sentence-Transformers (all-MiniLM-L6-v2)**: Open-source pre-trained transformer model for embedding text to a 384-dimensional dense vector space for tasks like clustering or semantic search.
- **Llama-2-7B-Chat**: Open-source fine-tuned Llama 2 model designed for chat dialogue. Leverages publicly available instruction datasets and over 1 million human annotations. 
- **Poetry**: Tool for dependency management and Python packaging

