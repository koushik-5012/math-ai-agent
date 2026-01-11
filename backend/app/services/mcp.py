import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing")

client = OpenAI()


def call_mcp(question: str, context: str = "") -> dict:
    system_prompt = """
You are a Math Professor AI.

Return ONLY valid JSON in this exact format:

{
  "final_answer": "...",
  "steps": ["step1", "step2"],
  "confidence": 0.0
}
"""

    user_prompt = f"""
Question:
{question}

Relevant Context:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except:
            return {
                "final_answer": raw,
                "steps": [],
                "confidence": 0.5
            }

    except Exception as e:
        return {
            "final_answer": "LLM service unavailable.",
            "steps": [],
            "confidence": 0.0,
            "error": str(e)
        }