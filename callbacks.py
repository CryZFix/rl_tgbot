from aiogram import Bot, F, Router, types


callback_router = Router()


@callback_router.callback_query(F.data.startswith("unban_"))
async def promo_process(callback_query: types.CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.data.split("_")[1]
    await bot.unban_chat_member(
        chat_id=callback_query.message.chat.id,
        user_id=int(user_id)
    )
    await callback_query.message.edit_reply_markup()
    await callback_query.message.edit_text("Пользователь разблокирован")
