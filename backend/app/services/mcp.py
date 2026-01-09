import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)


def call_mcp(question: str):
    system_prompt = """
You are Math Professor AI.

Return ONLY valid JSON in this format:

{
  "final_answer": "...",
  "steps": ["step1", "step2"],
  "confidence": 0.0
}
"""

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
        return json.loads(raw)
    except Exception as e:
        return {
            "final_answer": raw,
            "steps": [],
            "confidence": 0.5,
            "error": "Invalid JSON from model"
        }