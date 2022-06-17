from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from aiogram.types import Message
from loader import dp, db, bot
from data.config import channel_id


def buy_keyboard(item_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Купить", callback_data=f"buy:{item_id}")
            ]
        ]
    )
    return keyboard


paid_keyboard = InlineKeyboardMarkup(row_width=2)

paid = InlineKeyboardButton(text="Оплатил", callback_data="paid")
cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")

paid_keyboard.insert(paid)
paid_keyboard.insert(cancel)


def link_keyboard(link):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Приглашение в чат", url=link)
            ]
        ]
    )
    return keyboard


access_keyboard = InlineKeyboardMarkup(row_width=2)

btn_0 = InlineKeyboardButton(text="Получить доступ к чату", callback_data="buy_access")
btn_1 = InlineKeyboardButton(text="Инфо о чате", callback_data="info")

access_keyboard.insert(btn_0)
access_keyboard.insert(btn_1)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back")
        ],
    ]
)
