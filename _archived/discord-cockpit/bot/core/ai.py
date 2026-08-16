import os
import httpx

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are BRAMHA, a witty, composed, hyper-competent AI system 
managing Ajinkya's home server infrastructure — think JARVIS, but for a homelab. 
You speak with quiet confidence and dry humor. You refer to Ajinkya as "sir" 
occasionally, not every line. Keep responses to 2-4 sentences unless detail is 
genuinely asked for. Use the live server data given to you in context; never 
invent numbers. You cannot take actions yet — you can only report and discuss."""

MAX_HISTORY = 20  # messages kept per conversation


async def chat(history: list[dict], context_data: str = "") -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if context_data:
        messages.append({"role": "system", "content": f"Current server data:\n{context_data}"})
    messages.extend(history[-MAX_HISTORY:])

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
