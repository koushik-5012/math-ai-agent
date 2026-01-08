from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto"
)

def call_mcp(prompt: str) -> str:
    system_prompt = f"""
You are a senior mathematics professor.
Solve clearly with steps.

Question:
{prompt}

Answer:
"""

    inputs = tokenizer(system_prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=350,
        temperature=0.2,
        do_sample=True
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result.split("Answer:")[-1].strip()