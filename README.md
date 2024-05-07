# rl_tgbot


A simple bot for moderation and statistics of chat messages.


## Libraries used:
1. `aiogram` - For work with TelegramBotAPI
2. `aiosqlite` - As database (soon change to PostgreSQL)
3. `aiohttp` and `beautifulsoup4` - For parsing information of book
4. `apscheduler` - For task planning


## Necessary environment variables
`VK_API="PUT_HERE_TOKEN"`<br>
`VK_API_VERSION="5.199"`<br>
`VK_GROUP_ID=PUT_HERE_VK_GROUP_ID`<br>
`TG_API="PUT_HERE_BOT_TOKEN"`<br>
`TG_GROUP_ID=PUT_HERE_TG_GROUP_ID` - Needed for working scheduler<br>