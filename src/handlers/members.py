from aiogram import Bot, Router, types
from aiogram.filters import IS_ADMIN, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Bold, Text, TextMention
from aiogram.exceptions import TelegramBadRequest
from utils import db
from utils.cleaner import cleaner


router_chat_member = Router()


@router_chat_member.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: types.ChatMemberUpdated, bot: Bot):
    result = await db.get_user_left_count(user_id=event.new_chat_member.user.id)
    site_name = "Rulate.ru"
    buttons = [
        [InlineKeyboardButton(text="Нужна помощь, жми сюда 😉", url="t.me/Rulatemoder")],
        [InlineKeyboardButton(text="Правила чата", url="t.me/rulated/628354")],
        [InlineKeyboardButton(text="Стикеры нашего сообщества", url="t.me/addstickers/thomnuysticks")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    if result:
        text_message = Text(
            "Добро пожаловать домой, ",
            TextMention(event.new_chat_member.user.full_name, user=event.new_chat_member.user),
            "\nВы покидали нас ", result[1], " раз, рады что вы вернулись."
        )
        hello_msg = await event.answer(
            **text_message.as_kwargs(),
            reply_markup=keyboard,
            disable_web_page_preview=True,
            disable_notification=True
        )
    else:
        text_message = Text(
            "Добро пожаловать в чат ", Bold(site_name), ", ",
            TextMention(event.new_chat_member.user.full_name, user=event.new_chat_member.user),
            "\nЗдесь авторы, переводчики и читатели общаются друг с другом, ты также присоединяйся к дискуссии."
        )
        hello_msg = await event.answer(
            **text_message.as_kwargs(),
            reply_markup=keyboard,
            disable_web_page_preview=True,
            disable_notification=True
        )

    await cleaner(bot=bot, chat_id=event.chat.id,messages=[hello_msg.message_id], timeout=60)


@router_chat_member.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def left_member(event: types.ChatMemberUpdated, bot: Bot):
    text_message = Text(
        "К сожалению, пользователь \"",
        Bold(event.old_chat_member.user.full_name),
        "\" покидает нас.",
    )
    msg = await event.answer(**text_message.as_kwargs(), disable_web_page_preview=True, disable_notification=True)
    await cleaner(bot=bot, chat_id=event.chat.id, messages=[msg.message_id], timeout=60)
