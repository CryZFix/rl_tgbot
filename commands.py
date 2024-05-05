import asyncio

from aiogram import Bot, Router, types
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import BaseFilter, Command, CommandObject
from aiogram.methods.restrict_chat_member import ChatPermissions
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Bold, TextMention

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
        await bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[
                message.reply_to_message.message_id,
                message.message_id
            ]
        )
    except AttributeError:
        if not message.reply_to_message:
            attr_error = await message.reply(text="Вы не выбрали с каким сообщением производить действия")
            await asyncio.sleep(5)
            await attr_error.delete()
        pass
    except TelegramBadRequest as BadRequest:
        print(BadRequest)
    except TelegramNotFound as NotFound:
        print(NotFound)
