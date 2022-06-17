import sqlite3
from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from data.items import items
from keyboards.inline.purchases import buy_keyboard, paid_keyboard, link_keyboard
from loader import dp, db, bot
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney
from data.config import channel_id


@dp.callback_query_handler(text="buy_access")
async def show_items(call: types.CallbackQuery):
    caption = """
    Название продукта: {title}
Цена: {price:.2f} <b>RUB</b>
    """

    for item in items:
        await bot.send_message(call.from_user.id,
            caption.format(
                title = item.title,
                price = item.price,
            ),
            reply_markup=buy_keyboard(item_id=item.id)
        )


@dp.callback_query_handler(text_contains="buy")
async def create_invoice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(":")[-1]
    item_id = int(item_id) - 1
    item = items[item_id]

    amount = item.price
    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        "\n".join([
            f"Оплатите {amount:.2f} по ссылке",
            hlink("Ссылка на оплату", url=payment.invoice),
            ""
        ]),
        reply_markup=paid_keyboard)

    await state.set_state("qiwi")
    await state.update_data(payment=payment)

    @dp.callback_query_handler(text="cancel", state="qiwi")
    async def cancel_payment(call: types.CallbackQuery, state: FSMContext):
        await call.message.edit_text("Отменено")
        await state.finish()

    @dp.callback_query_handler(text="paid", state="qiwi")
    async def approve_payment(call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        payment: Payment = data.get("payment")
        try:
            payment.check_payment()
        except NoPaymentFound:
            await call.message.answer("Транзакция не найдена.")
            return
        except NotEnoughMoney:
            await call.message.answer("Оплаченная сумма меньше необходимой.")
            return

        else:
            expire_date = datetime.now() + timedelta(days=1)
            link = await bot.create_chat_invite_link(chat_id=channel_id, expire_date=expire_date.timestamp(),
            member_limit=1)
            link = link.invite_link
            link = str(link)
            await call.message.answer("Успешно оплачено", reply_markup=link_keyboard(link=link))
            name = call.from_user.full_name
            try:
                db.add_user(id=call.from_user.id,
                            name=name,
                            username=call.from_user.username,
                            date=call.message.date)
            except sqlite3.IntegrityError as err:
                print(err)
        await call.message.edit_reply_markup()
        await state.finish()
