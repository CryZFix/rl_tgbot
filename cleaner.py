import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def cleaner(bot: Bot, chat_id: int, messages: list[int], timeout: int) -> None:
    try:
        await asyncio.sleep(timeout)
        await bot.delete_messages(
            chat_id=chat_id,
            message_ids=messages
        )
    except TelegramBadRequest as BadRequest:
        print(BadRequest)


async def main():
    await cleaner(bot=bot, chat_id=chat_id, messages=messages, timeout="sad")
    