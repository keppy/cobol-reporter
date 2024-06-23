import os.path
import logging
import sys
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from pydantic import BaseModel
from openai import OpenAI
import instructor
from typing import Iterable, List

client = instructor.from_openai(OpenAI())

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    embed_model = OpenAIEmbedding()
    splitter =  SemanticSplitterNodeParser(
        buffer_size=1, breatpoint_percentile_threshold=95, embed_model=embed_model
    )
    # load the documents and create the index
    documents = SimpleDirectoryReader('data').load_data()
    nodes = splitter.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class SearchQuery(BaseModel):
    semantic_search: str

class MiltiPartResponse(BaseModel):
    response: str
    followups: List[str]
    sources: List[int]

def search(search: Iterable[SearchQuery]) -> str:
    print(f"Searching using ${search}")
    query_engine = index.as_query_engine(stream=True, similarity_top_k=1)
    for search in search:
        response = query_engine.query(search.semantic_search)
        return response

def extract_query(question: str) -> Iterable[SearchQuery]:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract a query"},
            {"role": "user", "content": question},
        ],
        response_model=Iterable[SearchQuery]
    )

def answer(question: str, results: str):
    prompt = f"answer {question} using context: {results}"
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        response_model=instructor.Partial[MiltiPartResponse]
    )

if __name__ == "__main__":
    from rich.console import Console

    while True:
        question: str = input("Ask a cobol question: ")

        search_query: SearchQuery = extract_query(question)
        results: str = search(search_query)

        print(f"search_query: {search_query}")
        print(f"Results: {results}")
        
        response = answer(question, results)

        console = Console()
        for r in response:
            console.clear()
            console.print(r.response)