import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_mcp(question: str, context: str = "") -> dict:
    system_prompt = """
You are Math Professor AI.

Return ONLY valid JSON exactly in this format:

{
  "final_answer": "...",
  "steps": ["step1", "step2"],
  "confidence": 0.0,
  "agent_trace": ["OCR","VectorSearch","MCPReasoning"]
}
"""

    user_prompt = f"""
Question:
{question}

Context:
{context}
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        raw = res.choices[0].message.content.strip()
        parsed = json.loads(raw)

        return parsed

    except Exception as e:
        return {
            "final_answer": "LLM unavailable.",
            "steps": [],
            "confidence": 0.0,
            "agent_trace": ["MCP_ERROR"],
            "error": str(e)
        }