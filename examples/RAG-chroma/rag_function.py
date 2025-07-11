import os
from typing import List, Sequence

import chromadb
from openai import OpenAI, AsyncOpenAI

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Inference.net API key – set this in your environment or a .env file
INFERENCE_API_KEY = os.getenv("INFERENCE_API_KEY")
if INFERENCE_API_KEY is None:
    raise RuntimeError(
        "INFERENCE_API_KEY environment variable not set.\n"
        "Grab an API key from https://inference.net/dashboard/api-keys and set it with:\n"
        "    export INFERENCE_API_KEY=your_key_here"
    )

# Embedding + chat models hosted on Inference.net (adjust as needed)
EMBED_MODEL = "text-embedding-ada-002"
CHAT_MODEL  = "meta-llama/llama-3.2-3b-instruct/fp-16"

# -----------------------------------------------------------------------------
# Clients
# -----------------------------------------------------------------------------

# Synchronous client (use AsyncOpenAI if you prefer async)
client = OpenAI(base_url="https://api.inference.net/v1", api_key=INFERENCE_API_KEY)

# Chroma client (defaults to local duckdb + parquet storage in ~/.chromadb)
chroma_client = chromadb.Client()

# Name a collection for your project. You can have many independent collections.
COLLECTION_NAME = "rag_documents"
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def _embed_texts(texts: Sequence[str]) -> List[List[float]]:
    """Embed a batch of texts using the Inference.net embedding endpoint."""
    response = client.embeddings.create(model=EMBED_MODEL, input=list(texts))
    # The OpenAI SDK returns Embedding objects with an `embedding` attribute
    return [d.embedding for d in response.data]


def add_documents(docs: Sequence[str], *, ids: Sequence[str] | None = None) -> None:
    """Add raw text documents to the Chroma collection.

    Parameters
    ----------
    docs : Sequence[str]
        The documents to be added.
    ids : Sequence[str] | None, optional
        Optional unique IDs. If omitted, they will be generated automatically.
    """
    if ids is None:
        ids = [f"doc_{i}" for i, _ in enumerate(docs)]
    if len(ids) != len(docs):
        raise ValueError("`ids` and `docs` must be the same length")

    embeddings = _embed_texts(docs)
    collection.add(ids=list(ids), documents=list(docs), embeddings=embeddings)


def rag_query(question: str, *, k: int = 3, temperature: float = 0.3) -> str:
    """Answer `question` using retrieved context from Chroma and an LLM.

    Steps:
    1. Embed the question and retrieve top-`k` relevant docs from Chroma.
    2. Craft a prompt that includes the docs as context.
    3. Call the Inference.net chat completion endpoint and return the answer.
    """
    # 1) Retrieve relevant docs
    question_embedding = _embed_texts([question])[0]
    query_res = collection.query(
        query_embeddings=[question_embedding],
        n_results=k,
        include=["documents", "ids", "distances"],
    )

    retrieved_docs = query_res["documents"][0] if query_res["documents"] else []

    # 2) Build a simple RAG prompt
    context_block = "\n\n".join(retrieved_docs) if retrieved_docs else "(no relevant context found)"
    user_prompt = (
        "Answer the question using the provided context.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Helpful answer:"
    )

    # 3) LLM call
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=temperature,
    )

    return completion.choices[0].message.content.strip()


# -----------------------------------------------------------------------------
# __main__ demo (run `python rag_function.py`)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import textwrap

    sample_docs = [
        "The Eiffel Tower is located in Paris and was completed in 1889.",
        "Mount Everest, on the border between Nepal and China, is the tallest mountain above sea level.",
        "The Pacific Ocean is the largest ocean on Earth, covering more than 60 million square miles."
    ]

    print("\nPopulating vector store with sample documents …")
    add_documents(sample_docs)

    query = "When was the Eiffel Tower built?"
    print(f"\nQuery: {query}\n")
    answer = rag_query(query)
    print("Answer:\n" + textwrap.fill(answer, width=80)) 