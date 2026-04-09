import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_explanation(headline, article, category, score):

	if not GROQ_API_KEY:
		return "Groq API key not configured."


	excerpt = article[:200]

	prompt = f"Headline: {headline}. Article exceprt: {article}. This was classfied as {category} with Confidence Percentage of {score}. In 1-2 sentences explain why."

	headers = {
		"Autorization" : f"Bearer {GROQ_API_KEY}",
		"Content-Type" : "application/json"
	}

	data = {
		"model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100
	}

	async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(GROQ_URL, json=data, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return "Explanation temporarily unavailable."