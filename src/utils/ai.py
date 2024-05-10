import asyncio
import os
import openai
from openai import AsyncOpenAI


async def answer_ai(message: str) -> str:
    while True:
        try:
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com")

            response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": message},
                ]
            )

            return response.choices[0].message.content
        except openai.InternalServerError:
            print("Сервер перегружен, повторная попытка")
            await asyncio.sleep(5)
