import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_mcp(question: str):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Solve this math problem step-by-step and return ONLY valid JSON:

{{
  "final_answer": "...",
  "steps": ["step1","step2"],
  "confidence": 0.0
}}

Question: {question}
"""
    )

    raw = response.output_text.strip()

    try:
        return json.loads(raw)
    except:
        return {"final_answer": raw, "steps": [], "confidence": 0.5}