import os
from openai import OpenAI

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY missing in environment")

client = OpenAI()

def embed_text(text: str):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding


def embed_batch(texts: list[str]):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [x.embedding for x in res.data]