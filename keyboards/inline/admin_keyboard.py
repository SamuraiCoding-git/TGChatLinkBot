from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Список пользователей",
                callback_data="users_list")
        ],

		[
            InlineKeyboardButton(
                text="Добавить пользователя",
                callback_data="add_user")
        ],
    ]
)


