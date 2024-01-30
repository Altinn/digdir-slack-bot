import timeit
import os
from typing import Sequence
from fastapi import FastAPI
import uvicorn
from typing import List
import pprint
from pydantic import BaseModel
from ragatouille import RAGPretrainedModel
import config

cfg = config.config()
pp = pprint.PrettyPrinter(indent=2)
app = FastAPI()

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")


class RerankRequest(BaseModel):
    user_input: str
    documents: List[str]


@app.post("/colbert/rerank")
async def rerank(request: RerankRequest):
    start = timeit.default_timer()
    content_original_rank = [
        document[:int(cfg.MAX_SOURCE_LENGTH / 3)]
        for document in request.documents
    ]
    reranked = RAG.rerank(query=request.user_input, documents=content_original_rank, k=10)
    duration = round(timeit.default_timer() - start, 1)
    print(f'Re-ranked {len(reranked)} documents in {duration} seconds.')
    return reranked



def main():
    import ssl
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='path/to/your/certificate.pem', keyfile='path/to/your/key.pem')
    uvicorn.run(app, host="0.0.0.0", port=3000, ssl_context=ssl_context)

if __name__ == "__main__":
    main()

