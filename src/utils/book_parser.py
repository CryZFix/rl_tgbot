import aiohttp

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BookParser:
    def __init__(self):
        self.response = None
        self.novel_url = None

    async def get_novel_page(self) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(url=self.novel_url, timeout=9)
                soup = BeautifulSoup(await response.text(), "lxml")
                age_check = soup.select_one("div.errorpage")
                if age_check:
                    payload = {
                        "path": self.novel_url,
                        "ok": "Да"
                    }
                    response = await session.post(
                        url="https://tl.rulate.ru/mature",
                        data=payload
                    )
                self.response = await response.text()
                return True
            except TimeoutError:
                print("Filed parse at link on chat", TimeoutError)
                return False
            except AttributeError:
                print("Filed parse at link on chat", AttributeError)
                return False

    async def parse_book_info(self, url: str) -> dict | None:
        try:
            self.novel_url = url
            result = await self.get_novel_page()
            if not result:
                return None

            novel_info = {}
            soup = BeautifulSoup(self.response, "lxml")

            novel_title = soup.select_one("div > h1").text
            novel_translate_status = soup.select_one(".tools > .info > dd").text

            possible_rating = soup.select_one("div.rating-block[data-action*='rate']")
            possible_quality = soup.select_one("div.rating-block[data-action*='quality_rate']")
            if possible_rating:
                rating = possible_rating.text.strip()
            else:
                rating = "Нет данных"
            if possible_quality:
                quality = possible_quality.text.strip()
            else:
                quality = "Нет данных"

            all_chapters = 0
            free_chapters = 0
            chapters = soup.select('tbody > tr.chapter_row')
            for chapter in chapters:
                check_buy = chapter.find('input')
                all_chapters += 1
                if 'data-price' not in str(check_buy):
                    free_chapters += 1

            possible_cover = soup.select_one("div#Info > div [data-slick-index='0'] img")
            if possible_cover:
                novel_cover = possible_cover.get("src")
            else:
                novel_cover = soup.select_one("div#Info > div img").get("src")

            possible_tags = soup.select("p > em > a[href*='genres']")
            if possible_tags:
                novel_tags = []
                for tag in possible_tags:
                    novel_tags.append(tag.text)
            else:
                novel_tags = ["не указаны"]

            novel_info["novel_title"] = novel_title
            novel_info["novel_cover"] = urljoin(base="https://rulate.ru", url=novel_cover)
            novel_info["novel_translate_status"] = novel_translate_status.strip("\n")
            novel_info["rating"] = rating
            novel_info["quality"] = quality
            novel_info["tags"] = novel_tags
            novel_info["all_chapters"] = all_chapters
            novel_info["free_chapters"] = free_chapters

            return novel_info
        except AttributeError:
            return None
