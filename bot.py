import asyncio
import os

import commands, callbacks

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.methods import DeleteWebhook


async def main():
    dp = Dispatcher()
    session = AiohttpSession(
        api=TelegramAPIServer.from_base('http://localhost:8081')
    )
    bot = Bot(token=os.environ['BOT_TOKEN'])
    dp.include_routers(
        commands.admin_command_router,
        callbacks.callback_router
    )

    await bot(DeleteWebhook(drop_pending_updates=True))
    asyncio.create_task(dp.start_polling(bot))
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
