import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env ONCE at import time
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

class LLMService:
    def generate_answer(self, question: str, context: str = "") -> str:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "You are a helpful math professor."},
                {"role": "user", "content": f"{context}\n\n{question}"}
            ]
        )
        return response.output_text.strip()