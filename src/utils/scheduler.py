import os

from aiogram import Bot
from aiogram.utils.formatting import Bold, Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import db

TG_GROUP_ID = os.getenv("TG_GROUP_ID")


async def initialize(bot: Bot) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily, args=[bot], trigger="cron", hour=23, minute=59, second=5)
    scheduler.add_job(send_weekly, args=[bot], trigger="cron", day_of_week='sun', hour=23, minute=59, second=10)
    scheduler.add_job(db.cleanup_messages_count, args=["day"], trigger="cron", hour=0, minute=0, second=5)
    scheduler.add_job(db.cleanup_messages_count, args=["week"], trigger="cron", day_of_week='mon', hour=0, minute=0, second=10)
    scheduler.add_job(db.cleanup_messages_count, args=["month"], trigger="cron", day=1, hour=0, minute=0, second=15)
    scheduler.start()
    print("Scheduler started")


async def send_daily(bot: Bot):
    result = await db.get_messages_stat(period="day")

    text_message = Text("Топ 10 балоболов чата за сегодня\n\n")
    for user in result:
        text_message += Text(Bold(user[1]), " сообщений: ", user[2], "\n")

    await bot.send_message(chat_id=TG_GROUP_ID, **text_message.as_kwargs())


async def send_weekly(bot: Bot):
    result = await db.get_messages_stat(period="week")

    text_message = Text("Топ 10 балоболов чата за неделю\n\n")
    for user in result:
        text_message += Text(Bold(user[1]), " сообщений: ", user[2], "\n")

    await bot.send_message(chat_id=TG_GROUP_ID, **text_message.as_kwargs())
