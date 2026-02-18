import json, re
from groq import Groq

MODEL = "llama-3.1-8b-instant"  # Groq model

def safe_json_loads(text):
    try:
        return json.loads(text)
    except:
        import re
        match = re.search(r'({.*}|\[.*\])', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    raise ValueError("Invalid JSON from LLM")

def call_llm(client, system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": str(system_prompt)},
            {"role": "user", "content": str(user_prompt)}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()
