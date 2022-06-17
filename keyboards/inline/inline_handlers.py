import os
import sqlite3
import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.test import User
from loader import dp, db, bot
from keyboards.inline.purchases import back_keyboard, access_keyboard, link_keyboard
from keyboards.inline.admin_keyboard import admin_keyboard
from data.config import channel_id


def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False


@dp.callback_query_handler(text="users_list")
async def users_list(call: types.CallbackQuery):
	users_id = db.select_all_users_id()
	print(users_id)
	users_name = db.select_all_users_name()
	users_username = db.select_all_users_username()
	users_date = db.select_all_users_date()
	my_file = open("data/users.txt", "w+")
	my_file.close()
	try:
		count = db.count_users()[0]
	except sqlite3.OperationalError:
		count = 0
	if not users_id:
		await call.message.edit_text("Нет пользователей")
		await call.message.answer(
			"\n".join(
				[
					f'Привет, админ: {call.from_user.full_name}!',
					f'В базе <b>{count}</b> пользователей',
				]), reply_markup=admin_keyboard)
	else:
		try:
			await call.message.edit_text("Список пользователей:")
		except aiogram.utils.exceptions.BadRequest:
			await call.message.delete()
			await call.message.answer("Список пользователей:")
		except aiogram.utils.exceptions.MessageToEditNotFound:
			print("Message to edit not found")
		x = -1
		for i in range(len(users_id)):
			my_file = open("data/users.txt", "a+")
			x = x + 1
			id = int(*users_id[x])
			names = str(*users_name[x])
			usernames = str(*users_username[x])
			dates = str(*users_date[x])
			string = f"{x + 1}. {id}, {names}, {usernames}, {dates}"
			my_file.writelines(f"{string}   ")
			my_file.close()
		await bot.send_document(call.from_user.id, open("data/users.txt", 'rb'), reply_markup=admin_keyboard)
		os.remove("data/users.txt")
	await call.message.edit_reply_markup()


@dp.callback_query_handler(text="info")
async def info(call: types.CallbackQuery):
	await call.message.edit_text("Пример текста о курсе")
	await call.message.edit_reply_markup(back_keyboard)


@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
	try:
		user_data = db.select_user(id=call.from_user.id)
	except sqlite3.OperationalError:
		user_data = None
	if not check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
		await call.message.edit_text(f'Привет, {call.from_user.full_name}!')
		await call.message.edit_reply_markup(access_keyboard)
	if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
		if user_data is None:
			await call.message.edit_text(f'Привет, {call.from_user.full_name}!')
			await call.message.edit_reply_markup(link_keyboard)


@dp.callback_query_handler(text="add_user")
async def add_user(call: types.CallbackQuery):
	await User.user_message.set()
	try:
		await call.message.edit_text("<b>Инструкция:</b>\n"
								 "\n"
								 "<b>1.</b> Попроси проверить пользователя пересылку сообщений\n"
								 "\n"
								 "Должно быть так ⬇️\n"
								 "\n"
								 "<b>Настройки - Конфиденциальность - Пересылка сообщений - Все</b>\n"
								 "\n"
								 "<b>2.</b> Перешли сообщение пользователя боту\n")
	except aiogram.utils.exceptions.BadRequest:
		await call.message.delete()
		await call.message.answer("<b>Инструкция:</b>\n"
								 "\n"
								 "<b>1.</b> Попроси проверить пользователя пересылку сообщений\n"
								 "\n"
								 "Должно быть так ⬇️\n"
								 "\n"
								 "<b>Настройки - Конфиденциальность - Пересылка сообщений - Все</b>\n"
								 "\n"
								 "<b>2.</b> Перешли сообщение пользователя боту\n")
	except aiogram.utils.exceptions.MessageToEditNotFound:
		print("Message to edit not found")
	await call.message.edit_reply_markup()
	await User.user_message.set()


@dp.message_handler(state=User.user_message)
async def add_user_handler(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data["user_message"] = message
		user_message = data["user_message"]
		try:
			db.add_user(id=user_message.forward_from.id,
						name=user_message.forward_from.full_name,
						username=user_message.forward_from.username,
						date=user_message.date)
			await message.answer(f"ID: {user_message.forward_from.id}\n"
								 f"Имя: {user_message.forward_from.full_name}\n"
								 f"Username: @{user_message.forward_from.username}\n"
								 f"Дата: {user_message.date}\n")

			await message.answer("Пользователь успешно добавлен", reply_markup=admin_keyboard)
			await state.finish()

		except sqlite3.IntegrityError as err:
			await state.finish()
			await message.answer("Что-то пошло не так..."
								 "Попробуй ещё раз", reply_markup=admin_keyboard)
			print(err)
	except AttributeError:
		await state.finish()
		await message.answer("Это не пересланное сообщение\n"
							 "Пришли ещё раз")
		await User.user_message.set()

		@dp.message_handler(state=User.user_message)
		async def error_user_message(message: types.Message, state: FSMContext):
			try:
				async with state.proxy() as data:
					data["user_message"] = message.forward_from.username
				user_message = data["user_message"]
				print(f"@{user_message}")
				try:
					db.add_user(id=user_message.forward_from.id,
								name=user_message.forward_from.full_name,
								username=user_message.forward_from.username,
								date=user_message.date)
					await message.answer(f"ID: {user_message.forward_from.id}\n"
										 f"Имя: {user_message.forward_from.full_name}\n"
										 f"Username: @{user_message.forward_from.username}\n"
										 f"Дата: {user_message.date}\n")

					await message.answer("Пользователь успешно добавлен", reply_markup=admin_keyboard)
					await state.finish()

				except sqlite3.IntegrityError as err:
					await state.finish()
					await message.answer("Что-то пошло не так..."
										 "Попробуй ещё раз", reply_markup=admin_keyboard)
					print(err)
			except AttributeError:
				await state.finish()
				await message.answer("Это не пересланное сообщение, нажми на кнопку еще раз",
									 reply_markup=admin_keyboard)
