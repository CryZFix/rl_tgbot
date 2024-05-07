import re

from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db, book_parser

message_router = Router()


@message_router.message(F.text)
async def message_counter(message: types.Message, bot: Bot):
    try:
        cleaned_message = re.sub(r'\W+', '', message.text).lower()
        pattern_kent = r".*[k|к|*][e|е|*|3][н|h|n|*][т|t|*].*"
        if (message.chat.type == "group" and not message.from_user.is_bot
                or message.chat.type == "supergroup" and not message.from_user.is_bot):
            await db.message_counter(user_id=message.from_user.id, user_first_name=message.from_user.first_name)
        if re.match(pattern=pattern_kent, string=cleaned_message):
            await message.reply_sticker(
                sticker="CAACAgIAAx0CVfdAjQABCB_AZaWNXTyKYRFhdX1RxReAaznMw5kAAjJEAAJ4u8FIYBju0SwbEPMzBA"
            )

        # book_pattern = r"https://[\w.]+\/book\/\d+"
        # match = re.search(book_pattern, message.text)
        # if match:
        #     parser = book_parser.BookParser()
        #     response = await parser.parse_book_info(url=match.group())
        #     if response:
        #         tags = ""
        #         for tag in response['tags']:
        #             tags += f"#{tag.replace(' ', '_')} "
        #         text_message = (
        #                         f"{response['novel_title']}\n"
        #                         f"<b>Статус книги:</b> {response['novel_translate_status']}\n"
        #                         f"<b>Жанры:</b> {tags}\n"
        #                         f"<b>Произведение:</b> {response['rating']}\n"
        #                         f"<b>Качество перевода:</b> {response['quality']}\n"
        #                         f"<b>Всего глав:</b> {response['all_chapters']}, из них {response['free_chapters']} бесплатных"
        #         )
        #         button = InlineKeyboardMarkup(
        #             inline_keyboard=[
        #                 [InlineKeyboardButton(text="Открыть книгу на сайте", url=match.group())]
        #             ]
        #         )
        #         await message.reply(text=text_message, reply_markup=button)
    except TelegramBadRequest:
        pass
