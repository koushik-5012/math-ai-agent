import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing in environment")

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str):
    """
    Create embedding vector for a single query.
    """
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

#------Function to embed batch of texts for KB ingestion------#
def embed_batch(texts: list[str]):
    """
    Create embedding vectors for KB ingestion.
    """
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [x.embedding for x in res.data]