import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.methods import DeleteWebhook

from commands import admins, set_commands, users
from handlers import callbacks, messages, members
from utils import scheduler, db


async def on_startup(bot: Bot):
    await set_commands.force_reset_all_commands(bot)
    await set_commands.set_chat_users_commands(bot)
    await set_commands.set_chat_admins_commands(bot)
    asyncio.create_task(scheduler.initialize(bot))


async def main():
    await db.init_db()
    dp = Dispatcher()
    session = AiohttpSession(
        api=TelegramAPIServer.from_base('http://localhost:8081')
    )
    bot = Bot(token=os.getenv("BOT_TOKEN"), session=session)
    dp.startup.register(on_startup)
    dp.include_routers(
        admins.admin_command_router,
        users.user_command_router,
        callbacks.callback_router,
        messages.message_router,
        members.router_chat_member
    )

    await bot(DeleteWebhook(drop_pending_updates=True))
    asyncio.create_task(dp.start_polling(bot))
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
