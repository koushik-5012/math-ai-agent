from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_answer(
        self,
        question: str,
        context: str,
        system_override: Optional[str] = None
    ) -> str:
        system_prompt = (
            system_override
            if system_override
            else "You are a helpful math professor. Explain clearly in plain text. Use LaTeX only when necessary."

        )

        messages = [
            {"role": "system", "content": system_prompt},
        ]

        if context:
            messages.append(
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{question}",
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        return response.choices[0].message.content
