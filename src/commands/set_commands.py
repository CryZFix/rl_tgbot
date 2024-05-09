from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllChatAdministrators, \
    BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats


async def force_reset_all_commands(bot: Bot):
    for scope in (
        BotCommandScopeAllGroupChats(),
        BotCommandScopeAllPrivateChats(),
        BotCommandScopeAllChatAdministrators(),
        BotCommandScopeAllPrivateChats(),
        BotCommandScopeDefault()
    ):
        await bot.delete_my_commands(scope=scope)


async def set_chat_users_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="rules", description="Отправить правила чата"),
            BotCommand(command="balabol", description="Топ говорливых бабок"),
            BotCommand(command="ai", description="Задать вопрос боту"),
        ],
        scope=BotCommandScopeAllGroupChats()
    )


async def set_chat_admins_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="ban", description="Бан пользователя (ответом)"),
            BotCommand(command="mute", description="Мут пользователя на N-минут (ответом)"),
            BotCommand(command="nomedia", description="Отобрать медиа и стикеры на N-минут (ответом)"),
            BotCommand(command="rules", description="Отправить правила чата"),
            BotCommand(command="balabol", description="Топ говорливых бабок")
        ],
        scope=BotCommandScopeAllChatAdministrators()
    )
