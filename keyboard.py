from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

push = ReplyKeyboardMarkup(keyboard=[
    [
         KeyboardButton(text='Меню')
    ],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Введите...', selective=True)
