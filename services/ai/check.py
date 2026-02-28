from google import genai
import json

from .prompts import make_check_prompt
from config import config


async def check_prompt(request: str):
    client = genai.Client(api_key=config.GEMINI_API)
    async with client.aio as aclient:
        response = await aclient.models.generate_content(
            model="gemini-2.5-flash",
            contents=make_check_prompt(request)
        )
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return True