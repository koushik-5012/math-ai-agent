import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load env once
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing. Set it in Railway variables.")

client = OpenAI(api_key=OPENAI_API_KEY)


def call_mcp(question: str) -> dict:
    system_prompt = """
You are Math Professor AI.

Return ONLY valid JSON exactly in this format:

{
  "final_answer": "...",
  "steps": ["step1", "step2", "..."],
  "confidence": 0.0
}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.2,
            max_tokens=500
        )

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
            return parsed
        except Exception:
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