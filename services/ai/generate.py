from google import genai
import json
import asyncio

from .prompts import make_prompt, MODEL
from config import config


async def generate_json(request: str):
    prompt = make_prompt(request)
    client = genai.Client(api_key=config.GEMINI_API)
    async with client.aio as aclient:
        response = await aclient.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {}