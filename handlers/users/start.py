import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import admins, channel_id
from keyboards.inline.purchases import link_keyboard
from keyboards.inline.admin_keyboard import admin_keyboard
from datetime import datetime, timedelta
from aiogram.types import Message
from loader import dp, db, bot


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        count = db.count_users()[0]
    except sqlite3.OperationalError:
        count = 0

    try:
        user_data = db.select_user(id=message.from_user.id)
    except sqlite3.OperationalError:
        user_data = None

    if message.from_user.id in admins:
        await message.answer(
            "\n".join(
                [
                    f'Привет, админ: {message.from_user.full_name}!',
                    f'В базе <b>{count}</b> пользователей',
                ]), reply_markup=admin_keyboard)
    else:
        if not check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
            await message.answer(
                "\n".join(
                    [
                        f'Привет, {message.from_user.full_name}!',
                    ]), reply_markup=link_keyboard)
        if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
            if user_data is None:
                await message.answer(
                    "\n".join(
                        [
                            f'Привет, {message.from_user.full_name}!',
                            'Ты не купил подписку и был удален из чата!'
                            'Чтобы купить доступ обратись к админу @ovsbts',
                        ]))
                await bot.kick_chat_member(chat_id=channel_id, user_id=message.from_user.id)
            else:
                expire_date = datetime.now() + timedelta(days=1)
                link = await bot.create_chat_invite_link(chat_id=channel_id, expire_date=expire_date.timestamp(),
                                                         member_limit=1)
                link = link.invite_link
                link = str(link)
                await message.answer(
                    "\n".join(
                        [
                            f'Привет, {message.from_user.full_name}!',
                        ]), reply_markup=link_keyboard(link=link))
