import aiohttp
import json
import os
import re

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
from datetime import datetime


class VkPolling:
    def __init__(self, bot):
        self.session = None
        self.bot = bot
        self.tg_group_id = os.getenv("TG_GROUP_ID")
        self.vk_api_version = os.getenv("VK_API_VERSION")
        self.vk_group_id = os.getenv("VK_GROUP_ID")
        self.vk_token = os.getenv("VK_API")
        self.vk_server = {}

    async def create_session(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.key_update, trigger="interval", minutes=10)

        self.session = aiohttp.ClientSession()
        params = {
            "access_token": self.vk_token,
            "group_id": self.vk_group_id,
            "v": self.vk_api_version
        }
        async with self.session.get(
                url="https://api.vk.com/method/groups.getLongPollServer",
                params=params
        ) as response:
            response = json.loads(await response.text())["response"]
            self.vk_server = {
                "ts": response["ts"],
                "server": response["server"],
                "key": response["key"],
            }
        scheduler.start()

    async def key_update(self):
        params = {
            "access_token": self.vk_token,
            "group_id": self.vk_group_id,
            "v": self.vk_api_version
        }
        async with self.session.get(
                url="https://api.vk.com/method/groups.getLongPollServer",
                params=params
        ) as response:
            response = json.loads(await response.text())["response"]
            self.vk_server = {
                "ts": response["ts"],
                "server": response["server"],
                "key": response["key"],
            }

    async def start_polling(self):
        await self.create_session()
        print("VK server polling started")
        while True:
            async with self.session.get(
                    url=self.vk_server["server"],
                    params={
                        "act": "a_check",
                        "key": self.vk_server["key"],
                        "ts": self.vk_server["ts"],
                        "wait": 60
                    }
            ) as response:
                try:
                    response = json.loads(await response.text())
                    if not response["updates"]:
                        continue
                    self.vk_server["ts"] = response["ts"]
                    if response["updates"][0]["type"] == "wall_post_new":
                        response = response["updates"][0]["object"]
                        if response["post_type"] == "post":
                            await self.new_post_handler(response=response)
                except IndexError:
                    pass
                    print(datetime.now(), "IndexError to get updates")
                    print("\n\n", response)
                    print(IndexError)
                except Exception as ex:
                    pass
                    print(datetime.now(), ex)

    async def new_post_handler(self, response):
        post_text = response["text"]
        post_attachments = response["attachments"]

        tg_post = {}
        attachments = {}
        if post_attachments:
            tg_post["image"] = None
            for attachment in post_attachments:
                if attachment["type"] == "photo":
                    image = attachment["photo"]["sizes"][-1]["url"]
                    tg_post["image"] = image
        else:
            tg_post["image"] = None

        tg_post["text"] = post_text if post_text else " "
        tg_post["attachments"] = attachments if attachments else None
        tg_post["vk_post_id"] = response["id"]
        await self.tg_repost(tg_post=tg_post, bot=self.bot)

    async def tg_repost(self, tg_post, bot):
        has_media = False
        text_message = tg_post["text"]

        like_button = InlineKeyboardButton(text="❤️ 0", callback_data="like")
        dislike_button = InlineKeyboardButton(text="💔 0", callback_data="dislike")

        pattern = r"https://[\w.]+\/book\/\d+"
        match = re.search(pattern, text_message)
        if match:
            button_to_book = InlineKeyboardButton(text="📖 Перейти к книге", url=match.group())
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [like_button, dislike_button],
                    [button_to_book]
                ]
            )
            rate, quality = await parse_rate(url=match.group())
            if rate and quality:
                text_message += "\n\n\nПроизведение: {}\nКачество перевода: {}".format(rate, quality)
            else:
                text_message += "\n"
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [like_button, dislike_button]
                ]
            )

        if tg_post["image"]:
            has_media = True

        text_message += '\n\n➰ <a href="https://vk.com/wall-{}_{}">ВК</a>'.format(
            self.vk_group_id,
            tg_post["vk_post_id"]
        )

        chaps_on_text = len(text_message)
        if chaps_on_text < 1024 and has_media:
            await bot.send_photo(
                chat_id=self.tg_group_id,
                photo=tg_post["image"],
                caption=text_message,
                reply_markup=keyboard
            )
        elif chaps_on_text >= 1024 and has_media:
            await bot.send_photo(
                chat_id=self.tg_group_id,
                photo=tg_post["image"],
            )
            await bot.send_message(chat_id=self.tg_group_id,
                                   text=text_message,
                                   disable_web_page_preview=True,
                                   reply_markup=keyboard
                                   )
        else:
            await bot.send_message(chat_id=self.tg_group_id,
                                   text=text_message,
                                   disable_web_page_preview=True,
                                   reply_markup=keyboard
                                   )


async def parse_rate(url):
    session = aiohttp.ClientSession()
    try:
        response = await session.get(url, timeout=5)
        soup = BeautifulSoup(await response.text(), "lxml")
        age_check = soup.select_one("div.errorpage")
        if age_check:
            payload = {
                "path": f"book/{url.split('book/')[1]}",
                "ok": "Да"
            }
            page = await session.post("https://tl.rulate.ru/mature", data=payload, timeout=10)
            soup = BeautifulSoup(await page.text(), "lxml")
        rate = soup.select("div.rating-block")
        rating = rate[0].text.strip()
        quality = rate[1].text.strip()
        await session.close()
        return rating, quality
    except TimeoutError:
        await session.close()
        return None, None
    except AttributeError:
        await session.close()
        return None, None