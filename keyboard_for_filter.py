from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

buttons = InlineKeyboardBuilder()
buttons.add(types.InlineKeyboardButton(text='📊 Рейтинг от', callback_data='rating_from'))
buttons.add(types.InlineKeyboardButton(text='📊 Рейтинг до', callback_data='rating_before'))
buttons.row(types.InlineKeyboardButton(text='Год от', callback_data='year_from'))
buttons.add(types.InlineKeyboardButton(text='Год до', callback_data='year_to'))
buttons.row(types.InlineKeyboardButton(text='🎬 Выбрать жанр', callback_data='genre'))
buttons.row(types.InlineKeyboardButton(text='Выбрать страну', callback_data='country'))
buttons.row(types.InlineKeyboardButton(text='♻️ Сбросить', callback_data='cancel_all'))
buttons.add(types.InlineKeyboardButton(text='✅ Искать', callback_data='confirm'))

class UserFilter:
    def __init__(self):
        self.rating_from = ""
        self.rating_before = ""
        self.year_from = ""
        self.year_to = ""
        self.type = ""
        self.country = ""

    def set_rating_from(self, rating_from):
        self.rating_from = rating_from

    def set_rating_before(self, rating_before):
        self.rating_before = rating_before

    def set_year_from(self, year_from):
        self.year_from = year_from

    def set_year_to(self, year_to):
        self.year_to = year_to
    def set_type(self, type):
        self.type = type

    def set_country(self, country):
        self.country = country
    def get_rating_from(self):
        return self.rating_from

    def get_rating_before(self):
        return self.rating_before

    def get_year_from(self):
        return self.year_from

    def get_year_to(self):
        return self.year_to

    def get_type(self):
        return self.type

    def get_country(self):
        return self.country

    def __dict__(self):
        return self.__dict__