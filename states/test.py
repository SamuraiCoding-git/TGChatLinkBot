from aiogram.dispatcher.filters.state import StatesGroup, State

class User(StatesGroup):
    user_message = State()