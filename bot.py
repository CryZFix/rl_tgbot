import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.methods import DeleteWebhook

import callbacks
import commands
import set_commands


async def on_startup(bot: Bot):
    await set_commands.force_reset_all_commands(bot)
    await set_commands.set_chat_users_commands(bot)
    await set_commands.set_chat_admins_commands(bot)


async def main():
    dp = Dispatcher()
    session = AiohttpSession(
        api=TelegramAPIServer.from_base('http://localhost:8081')
    )
    bot = Bot(token=os.environ['BOT_TOKEN'])
    dp.startup.register(on_startup)
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
