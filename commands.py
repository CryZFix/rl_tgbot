import time

from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.methods.restrict_chat_member import ChatPermissions
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Bold, TextMention

from cleaner import cleaner


admin_command_router = Router()


@admin_command_router.message(Command("ban"))
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
    except AttributeError:
        if not message.reply_to_message:
            attr_error = await message.reply(text="Команда должна быть вызвана в ответ на сообщение")
            await cleaner(bot=bot, chat_id=message.chat.id, messages=[attr_error.message_id], timeout=10)
    except TelegramBadRequest as BadRequest:
        print(BadRequest)
    except TelegramNotFound as NotFound:
        print(NotFound)


@admin_command_router.message(Command("mute"))
async def mute_command(message: types.Message, bot: Bot, command: CommandObject):
    try:
        mute_time = int(command.args) if command.args else 5
        mute_time = mute_time if mute_time > 1 else 1
        mute_time = mute_time if mute_time < 300 else 300
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
        await bot.send_message(**content.as_kwargs(), disable_web_page_preview=True)
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[message.message_id], timeout=0)
    except AttributeError as AttrError:
        if not message.reply_to_message:
            attr_error = await message.reply(text="Команда должна быть вызвана в ответ на сообщение")
            await cleaner(
                bot=bot,
                chat_id=message.chat.id,
                messages=[message.message_id, attr_error.message_id],
                timeout=10
            )
        else:
            print(AttrError)
    except TelegramBadRequest as BadRequest:
        print(BadRequest)


@admin_command_router.message(Command("nomedia"))
async def mute_command(message: types.Message, bot: Bot, command: CommandObject):
    try:
        mute_time = int(command.args) if command.args else 5
        mute_time = mute_time if mute_time > 1 else 1
        mute_time = mute_time if mute_time < 300 else 300
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
        await bot.send_message(**content.as_kwargs(), disable_web_page_preview=True)
        await cleaner(bot=bot, chat_id=message.chat.id, messages=[message.message_id], timeout=0)
    except AttributeError as AttrError:
        if not message.reply_to_message:
            attr_error = await message.reply(text="Команда должна быть вызвана в ответ на сообщение")
            await cleaner(
                bot=bot,
                chat_id=message.chat.id,
                messages=[message.message_id, attr_error.message_id],
                timeout=10
            )
        else:
            print(AttrError)
    except TelegramBadRequest as BadRequest:
        print(BadRequest)
