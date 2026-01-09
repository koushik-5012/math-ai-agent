import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_mcp(question: str):
    """
    Calls OpenAI to solve math questions and return structured reasoning.
    """

    system_prompt = """
You are Math Professor AI.

You must return output strictly in this JSON format:

{
  "final_answer": "...",
  "steps": ["step1", "step2", "..."],
  "confidence": 0.0-1.0
}

Answer clearly with full reasoning steps.
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
        return eval(raw)   # MCP returns structured JSON-like output
    except:
        return {
            "final_answer": raw,
            "steps": [],
            "confidence": 0.5
        }
