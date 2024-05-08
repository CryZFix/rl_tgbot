import time

from aiogram import Bot, Router, types
from aiogram.filters import BaseFilter, Command, CommandObject
from aiogram.methods.restrict_chat_member import ChatPermissions
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Bold, TextMention

from utils import db
from utils.cleaner import cleaner


admin_command_router = Router()


class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message, bot: Bot):
        access = await db.get_admins(user_id=message.from_user.id)
        if not message.reply_to_message:
            attr_error = await message.reply(text="Команда должна быть вызвана в ответ на сообщение")
            await cleaner(
                bot=bot,
                chat_id=message.chat.id,
                messages=[message.message_id, attr_error.message_id],
                timeout=10
            )
            return
        if access:
            return True
        msg = await message.reply("У вас нет доступа к этой команде.")
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[msg.message_id], timeout=5)


@admin_command_router.message(Command("ban"), AdminFilter())
async def ban_command(message: types.Message, bot: Bot, command: CommandObject) -> None:
    try:
        reason = command.args if command.args else "Не указана"
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            revoke_messages=True
        )
        content = Text(
            "Пользователь ",
            TextMention(message.reply_to_message.from_user.full_name, user=message.reply_to_message.from_user),
            " был заблокирован.\n"
            "Администратором: ",
            TextMention(message.from_user.full_name, user=message.from_user),
            "\nПричина: ",
            Bold(reason)
        )
        await message.answer(
            **content.as_kwargs(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Разблокировать",
                            callback_data=f"unban_{message.reply_to_message.from_user.id}"
                        )
                    ]
                ]
            )
        )
        await cleaner(
            bot=bot,
            chat_id=message.chat.id,
            messages=[message.message_id, message.reply_to_message.message_id],
            timeout=0
        )
    except TelegramBadRequest as BadRequest:
        print(BadRequest)
    except TelegramNotFound as NotFound:
        print(NotFound)


@admin_command_router.message(Command("mute"), AdminFilter())
async def mute_command(message: types.Message, bot: Bot, command: CommandObject) -> None:
    try:
        mute_time = int(command.args) if command.args else 5
        mute_time = mute_time if mute_time > 1 else 1
        mute_time = mute_time if mute_time < 360 else 360
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=False
            ),
            until_date=int(time.time()) + mute_time*60,
        )
        content = Text(
            "Пользователь ",
            TextMention(message.reply_to_message.from_user.full_name, user=message.reply_to_message.from_user),
            " потерял(а) возможность писать в чат на ",
            Bold(str(mute_time)),
            " минут.\n",
            "Администратор: ",
            TextMention(message.from_user.full_name, user=message.from_user)
        )
        await message.answer(**content.as_kwargs(), disable_web_page_preview=True)
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[message.message_id], timeout=0)
    except TelegramBadRequest as BadRequest:
        print(BadRequest)


@admin_command_router.message(Command("nomedia"), AdminFilter())
async def nomedia_command(message: types.Message, bot: Bot, command: CommandObject) -> None:
    try:
        mute_time = int(command.args) if command.args else 5
        mute_time = mute_time if mute_time > 1 else 1
        mute_time = mute_time if mute_time < 360 else 360
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_photos=False,
                can_send_videos=False,
                can_send_documents=False
            ),
            until_date=int(time.time()) + mute_time*60,
        )
        content = Text(
            "Пользователь ",
            TextMention(message.reply_to_message.from_user.full_name, user=message.reply_to_message.from_user),
            " потерял(а) возможность отправлять медиа-файлы и стикеры в чат на ",
            Bold(str(mute_time)),
            " минут.\n",
            "Администратор: ",
            TextMention(message.from_user.full_name, user=message.from_user)
        )
        await message.answer(**content.as_kwargs(), disable_web_page_preview=True)
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[message.message_id], timeout=0)
    except TelegramBadRequest as BadRequest:
        print(BadRequest)
