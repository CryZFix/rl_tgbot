import asyncio

from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter

from utils import db
from utils.cleaner import cleaner


callback_router = Router()


class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message, bot: Bot, callback_query: types.CallbackQuery):
        access = await db.get_admins(user_id=message.from_user.id)
        if access:
            return True
        if callback_query:
            await bot.answer_callback_query(callback_query.id)
        msg = await message.reply("У вас нет доступа к этой команде.")
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[msg.message_id], timeout=5)


@callback_router.callback_query(F.data.startswith("unban_"), AdminFilter())
async def promo_process(callback_query: types.CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.data.split("_")[1]
    await bot.unban_chat_member(
        chat_id=callback_query.message.chat.id,
        user_id=int(user_id)
    )
    await callback_query.message.edit_reply_markup()
    await callback_query.message.edit_text("Пользователь разблокирован")


@callback_router.callback_query(lambda c: c.data == "like" or c.data == "dislike")
async def like_and_dislike(callback_query: types.CallbackQuery, bot: Bot):
    try:
        if await db.get_clicked_user(callback_query.from_user.id, callback_query.message.message_id):
            await bot.answer_callback_query(callback_query.id, text="Вы уже оставили мнение")
            return
        if callback_query.data == 'like':
            like_count = int(callback_query.message.reply_markup.inline_keyboard[0][0].text.split()[1])
            like_count += 1
            callback_query.message.reply_markup.inline_keyboard[0][0].text = f"❤️ {like_count}"
            await bot.answer_callback_query(callback_query.id)
            await db.add_clicked_user(callback_query.from_user.id, callback_query.message.message_id)
        if callback_query.data == 'dislike':
            dislike_count = int(callback_query.message.reply_markup.inline_keyboard[0][1].text.split()[1])
            dislike_count += 1
            callback_query.message.reply_markup.inline_keyboard[0][1].text = f"💔 {dislike_count}"
            await bot.answer_callback_query(callback_query.id)
            await db.add_clicked_user(callback_query.from_user.id, callback_query.message.message_id)
        await bot.edit_message_reply_markup(
            callback_query.message.chat.id, callback_query.message.message_id,
            reply_markup=callback_query.message.reply_markup
        )
    except TelegramBadRequest:
        pass


@callback_router.callback_query(lambda c: c.data == "s_day" or "s_week" or "s_month" or "s_all")
async def get_messages_count_stat(callback_query: types.CallbackQuery, bot: Bot) -> None:
    try:
        if callback_query.data == "s_all":
            result = await db.get_messages_stat()
            text_message = "Топ 10 балоболов чата за все время\n\n"
        elif callback_query.data == "s_day":
            result = await db.get_messages_stat(period="day")
            text_message = "Топ 10 балоболов чата за сегодня\n\n"
        elif callback_query.data == "s_week":
            result = await db.get_messages_stat(period="week")
            text_message = "Топ 10 балоболов чата за неделю\n\n"
        elif callback_query.data == "s_month":
            result = await db.get_messages_stat(period="month")
            text_message = "Топ 10 балоболов чата за месяц\n\n"
        else:
            return
        await bot.answer_callback_query(callback_query.id)

        for user in result:
            text_message += f"<b>{user[1]}</b>, сообщений: {user[2]}\n"

        if callback_query.from_user.id not in result:
            result = await db.get_me_messages_stat(user_id=callback_query.from_user.id, period=callback_query.data)
            text_message += f"\n\nТоп вызвал <b>{callback_query.from_user.first_name}</b>, сообщений: {result[0]}"

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=text_message
        )

        await asyncio.sleep(60)
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
    except TelegramBadRequest:
        pass
