from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import Text, Bold, TextMention
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from utils import ai
from utils.cleaner import cleaner


user_command_router = Router()


@user_command_router.message(Command("ai"))
async def ai_answer(message: types.Message) -> None:
    try:
        answer = await ai.answer_ai(message.text)
        await message.reply(answer)
    except TelegramBadRequest:
        pass


@user_command_router.message(Command("rules", "правила"))
async def show_rules(message: types.Message, bot: Bot) -> None:
    try:
        await message.delete()
        button = [
            [InlineKeyboardButton(text="Правила чата", url="t.me/rulated/628354")]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=button)
        content = Text(
            TextMention(message.from_user.full_name, user=message.from_user),
            Bold(" настаивает на ознакомлении с правилами")
        )
        rules = await message.answer(**content.as_kwargs(), reply_markup=keyboard)
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[rules.message_id], timeout=60)
    except TelegramBadRequest:
        pass


@user_command_router.message(Command("balabol", "балабол"))
async def show_stats(message: types.Message) -> None:
    button = [
        [
            InlineKeyboardButton(text="День", callback_data="s_day"),
            InlineKeyboardButton(text="Неделя", callback_data="s_week"),
            InlineKeyboardButton(text="Месяц", callback_data="s_month")
        ],
        [InlineKeyboardButton(text="Всё время", callback_data="s_all")]
    ]
    await message.reply(
        text="За какой период времени хотите показать статистику?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=button)
    )
    await message.delete()


@user_command_router.message(Command("pornhub", "pornohub", "ph"))
async def send_no_fap_message(message: types.Message) -> None:
    await message.reply_photo(
        photo="https://img10.reactor.cc/pics/post/Picrandom-разное-5249150.jpeg"
    )
