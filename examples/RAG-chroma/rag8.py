import os, chromadb; from openai import OpenAI
c = OpenAI(base_url="https://api.inference.net/v1", api_key=os.getenv("INFERENCE_API_KEY"))
db = chromadb.Client().get_or_create_collection("rag")

def rag(q, docs=None, k: int = 3, model="meta-llama/llama-3.2-3b-instruct/fp-16", embed="text-embedding-ada-002"):
    if docs: db.add(ids=[str(i) for i in range(len(docs))], documents=docs, embeddings=c.embeddings.create(model=embed, input=docs).data)
    res = db.query(query_embeddings=[c.embeddings.create(model=embed, input=[q]).data[0]], n_results=k, include=["documents"])["documents"][0]
    msg = f"Answer using context:\n{'\n'.join(res)}\n\nQuestion: {q}\nAnswer:"
    return c.chat.completions.create(model=model, messages=[{"role": "user", "content": msg}]).choices[0].message.content 