# Digdir Slack bot 

This is an early version of a general purpose Generative AI Assistant, hosted as a Slack app. 

The goal is to rapidly prototype core GenAI concepts to support Altinn 3 app developers by better leveragine the rich data sources already available. 

The main data sources on the evaluation list include:

- Altinn 3 Studio documentation, schema files and source code
- Publicly available Altinn 3 app source code
- Slack conversation history related to developer support


## RAG concepts

_add description and background references here_


_add sequence diagram for RAG with query understanding here_

```mermaid
sequenceDiagram    
    participant slack-backend
    participant docs-qa-bot
    participant typesense-query-api
    participant openai-gpt-4-api 
    participant openai-embeddings-api

    slack-backend-)docs-qa-bot: new message event
    docs-qa-bot->>+typesense-query-api: POST /multi_query - free text input
    typesense-query-api-->>-docs-qa-bot: ranked document set
    docs-qa-bot->>+typesense-query-api: GET /documents w/embeddings
    typesense-query-api-->>-docs-qa-bot: documents with embeddings
    docs-qa-bot->>+openai-embeddings-api: create embeddings if missing
    openai-embeddings-api-->>-docs-qa-bot: OpenAI embeddings
    docs-qa-bot->>+openai-gpt-4-api: Chat completion with embeddings
    openai-gpt-4-api-->>-docs-qa-bot: Chat continuation
    docs-qa-bot-)slack-backend: Formatted chat response as new Slack message
```


## Local development


### Producing derived data sets from code repositories

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

