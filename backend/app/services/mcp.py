from openai import OpenAI
import os, re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_mcp(question: str) -> dict:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Solve step by step and end with: Final Answer:"},
            {"role": "user", "content": question}
        ]
    )

    text = res.choices[0].message.content.strip()

    steps = []
    answer = text

    if "Final Answer:" in text:
        body, answer = text.split("Final Answer:")
        for line in body.split("\n"):
            line = re.sub(r"^\d+\.\s*", "", line).strip()
            if line:
                steps.append(line)

    return {
        "final_answer": answer.strip(),
        "steps": steps,
        "confidence": 0.75
    }
