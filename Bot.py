import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import URLInputFile
from keyboard_for_filter import UserFilter, buttons

from keyboard import push
from filter_rating_keyboard import keyboard_builder, keyboard_builder2, rating_from_map, rating_before_map
from filter_country_keyboard import keyboard_builder3, country_map
from filter_genre_keyboard import keyboard_builder4, genre_map
from filter_year_keyboard import keyboard_builder5, keyboard_builder6

from find_movie import get_random_movie, get_new_movie, by_filter_get, get_movie_info, show_info_about_movie, get_popular_movie, show_info_about_movie2
from database import delete_movie_from_list

token_ = "..." #put your token before start 
  
conn = sqlite3.connect('movie_bot.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                  (user_id INTEGER, movie TEXT)''')

bot = Bot(token=token_)
dispatcher = Dispatcher(storage=MemoryStorage())

user_filters = {}
user_films = {}
@dispatcher.message(Command("start"))
async def start(message: types.Message):
    if not (message.from_user.id in user_filters):
        user_filters[message.from_user.id] = UserFilter()
    text_ = f"""
    Привет, {message.from_user.full_name}!

Я - бот для подборки фильмов, мультфильмов и сериалов.
Для получения списка команд и работы введите /menu.
    """
    await message.answer(text=text_, reply_markup = push)

@dispatcher.message(Command("menu"))
async def menu(message: types.Message):
    if not (message.from_user.id in user_filters):
        user_filters[message.from_user.id] = UserFilter()

    buttons = InlineKeyboardBuilder()
    buttons.add(types.InlineKeyboardButton(text='👀 О нас', callback_data='about_us'))
    buttons.add(types.InlineKeyboardButton(text='❤️ Избранное', callback_data='favorite'))
    buttons.row(types.InlineKeyboardButton(text='🎲 Случайный выбор из ТОП-250', callback_data='random'))
    buttons.row(types.InlineKeyboardButton(text='⚙️ Фильтр', callback_data='filter'))
    buttons.row(types.InlineKeyboardButton(text='🔝 Популярное', callback_data='popular'))
    buttons.add(types.InlineKeyboardButton(text='🆕 Новинки', callback_data='new'))
    buttons.row(types.InlineKeyboardButton(text='🔍 Начать поиск', callback_data='search'))
    text_ = "Меню"
    await message.answer(text=text_, reply_markup = buttons.as_markup())

@dispatcher.message(F.text.lower() == "меню")
async def menu(message: types.Message):
    if not (message.from_user.id in user_filters):
        user_filters[message.from_user.id] = UserFilter()

    buttons = InlineKeyboardBuilder()
    buttons.add(types.InlineKeyboardButton(text='👀 О нас', callback_data='about_us'))
    buttons.add(types.InlineKeyboardButton(text='❤️ Избранное', callback_data='favorite'))
    buttons.row(types.InlineKeyboardButton(text='🎲 Случайный выбор из ТОП-250', callback_data='random'))
    buttons.row(types.InlineKeyboardButton(text='⚙️ Фильтр', callback_data='filter'))
    buttons.row(types.InlineKeyboardButton(text='🔝 Популярное', callback_data='popular'))
    buttons.add(types.InlineKeyboardButton(text='🆕 Новинки', callback_data='new'))
    buttons.row(types.InlineKeyboardButton(text='🔍 Начать поиск', callback_data='search'))
    text_ = "Меню"
    await message.answer(text=text_, reply_markup=buttons.as_markup())



@dispatcher.callback_query(F.data == "about_us")
async def info_about_us(callback):
    text_ = ("Всем привет 👋 \n"
             "Мы студенты 2 курса ОП «Прикладная математика и информатика». \n"
             "Данный бот - результат нашего проекта по Python 🎉 \n")
    await callback.message.answer(text=text_)
@dispatcher.callback_query(F.data == "favorite")
async def info_about_favourite(callback):
    # text_ = "Ваши любимые произведения\n"
    # await callback.message.answer(text=text_)

    user_id = callback.from_user.id
    cursor.execute("SELECT movie FROM movies WHERE user_id=?", (user_id,))
    movies = cursor.fetchall()

    buttons_ = InlineKeyboardBuilder()
    buttons_.add(types.InlineKeyboardButton(text='Очистить содержимое', callback_data='clear_favourite'))

    if len(movies) > 0:
        movies = list(set(movies))
        movie_list = "\n".join([movie[0] for movie in movies])
        await callback.message.answer(f"Ваши фильмы：\n{movie_list}", reply_markup=buttons_.as_markup())
    else:
        await callback.message.answer("Нет фильмов", reply_markup=buttons_.as_markup())




@dispatcher.callback_query(F.data == "filter")
async def filter(callback):
    chosen_ = "✔️ Выбрано : "
    if (user_filters[callback.from_user.id].get_rating_before() == "" and user_filters[callback.from_user.id].get_rating_from() != ""):
        user_filters[callback.from_user.id].set_rating_before(10)
        rating_ = "➡️ Рейтинг : " + str(user_filters[callback.from_user.id].get_rating_from()) + " - " + str(user_filters[callback.from_user.id].get_rating_before())
    elif (user_filters[callback.from_user.id].get_rating_before() != "" and user_filters[callback.from_user.id].get_rating_from() == ""):
        user_filters[callback.from_user.id].set_rating_from(0)
        rating_ = "➡️ Рейтинг : " + str(user_filters[callback.from_user.id].get_rating_from()) + " - " + str(user_filters[callback.from_user.id].get_rating_before())
    elif (user_filters[callback.from_user.id].get_rating_before() == "" and user_filters[callback.from_user.id].get_rating_from() == ""):
        rating_ = "➡️ Рейтинг : "
    elif (user_filters[callback.from_user.id].get_rating_before() < user_filters[callback.from_user.id].get_rating_from()):
        rating_ = "➡️ Рейтинг : " + str(user_filters[callback.from_user.id].get_rating_from()) + " - " + str(user_filters[callback.from_user.id].get_rating_from())
    else:
        rating_ = "➡️ Рейтинг : " + str(user_filters[callback.from_user.id].get_rating_from()) + " - " + str(user_filters[callback.from_user.id].get_rating_before())

    if (user_filters[callback.from_user.id].get_year_to() == "" and user_filters[callback.from_user.id].get_year_from() != ""):
        user_filters[callback.from_user.id].set_year_to(2023)
        year_ = "➡️ Год : " + str(user_filters[callback.from_user.id].get_year_from()) + " - " + str(user_filters[callback.from_user.id].get_year_to())
    elif (user_filters[callback.from_user.id].get_year_to() != "" and user_filters[callback.from_user.id].get_year_from() == ""):
        user_filters[callback.from_user.id].set_year_from(1960)
        year_ = "➡️ Год : " + str(user_filters[callback.from_user.id].get_year_from()) + " - " + str(user_filters[callback.from_user.id].get_year_to())
    elif (user_filters[callback.from_user.id].get_year_to() == "" and user_filters[callback.from_user.id].get_year_from() == ""):
        year_ = "➡️ Год : "
    elif (user_filters[callback.from_user.id].get_year_to() < user_filters[callback.from_user.id].get_year_from()):
        year_ = "➡️ Год : " + str(user_filters[callback.from_user.id].get_year_from()) + " - " + str(user_filters[callback.from_user.id].get_year_from())
    else:
        year_ = "➡️ Год : " + str(user_filters[callback.from_user.id].get_year_from()) + " - " + str(user_filters[callback.from_user.id].get_year_to())

    type_ = "➡️ Жанр : " + str(user_filters[callback.from_user.id].get_type())
    country_ = "➡️ Страна : " + str(user_filters[callback.from_user.id].get_country())

    text_ = chosen_ + '\n' + rating_ + '\n' + year_ + '\n' + type_ + '\n' + country_

    await callback.message.answer(text=text_, reply_markup = buttons.as_markup())

@dispatcher.callback_query(F.data == "rating_from")
async def rating_from(callback):
    await callback.message.answer('Выберите число:', reply_markup=keyboard_builder.as_markup())

@dispatcher.callback_query(F.data.in_(rating_from_map))
async def process_rating_from(callback):
    data = callback.data
    rating = rating_from_map[data]
    user_filters[callback.from_user.id].set_rating_from(rating)
    await filter(callback)

@dispatcher.callback_query(F.data == "rating_before")
async def rating_from(callback):
    await callback.message.answer('Выберите число:', reply_markup=keyboard_builder2.as_markup())

@dispatcher.callback_query(F.data.in_(rating_before_map))
async def process_rating_before(callback):
    data = callback.data
    rating = rating_before_map[data]
    user_filters[callback.from_user.id].set_rating_before(rating)
    await filter(callback)

@dispatcher.callback_query(F.data == "country")
async def country(callback):
    await callback.message.answer('Выберите страну:', reply_markup=keyboard_builder3.as_markup())

@dispatcher.callback_query(F.data.in_(country_map))
async def process_country(callback):
    data = callback.data
    country = country_map[data]
    user_filters[callback.from_user.id].set_country(country)
    await filter(callback)

@dispatcher.callback_query(F.data == "genre")
async def genre(callback):
    await callback.message.answer('Выберите жанр:', reply_markup=keyboard_builder4.as_markup())

@dispatcher.callback_query(F.data.in_(genre_map))
async def process_genre(callback):
    data = callback.data
    genre = genre_map[data]
    user_filters[callback.from_user.id].set_type(genre)
    await filter(callback)

@dispatcher.callback_query(F.data == "cancel_all")
async def cancel_all(callback):
    user_filters[callback.from_user.id].set_rating_from("")
    user_filters[callback.from_user.id].set_rating_before("")
    user_filters[callback.from_user.id].set_year_from("")
    user_filters[callback.from_user.id].set_year_to("")
    user_filters[callback.from_user.id].set_type("")
    user_filters[callback.from_user.id].set_country("")
    await callback.message.answer('Фильтр сброшен')
    await filter(callback)

@dispatcher.callback_query(F.data == "year_from")
async def year_from(callback):
    await callback.message.answer('Выберите год:', reply_markup=keyboard_builder5.as_markup())

@dispatcher.callback_query(F.data == "s2023")
@dispatcher.callback_query(F.data == "s2022")
@dispatcher.callback_query(F.data == "s2021")
@dispatcher.callback_query(F.data == "s2020")
@dispatcher.callback_query(F.data == "s2018")
@dispatcher.callback_query(F.data == "s2016")
@dispatcher.callback_query(F.data == "s2014")
@dispatcher.callback_query(F.data == "s2012")
@dispatcher.callback_query(F.data == "s2010")
@dispatcher.callback_query(F.data == "s2005")
@dispatcher.callback_query(F.data == "s2000")
@dispatcher.callback_query(F.data == "s1990")
@dispatcher.callback_query(F.data == "s1980")
@dispatcher.callback_query(F.data == "s1970")
@dispatcher.callback_query(F.data == "s1960")
async def filter_by_year_from(callback):
    year = int(callback.data[1:])
    user_filters[callback.from_user.id].set_year_from(year)
    await filter(callback)

@dispatcher.callback_query(F.data == "year_to")
async def year_to(callback):
    await callback.message.answer('Выберите год:', reply_markup=keyboard_builder6.as_markup())

@dispatcher.callback_query(F.data == "f2023")
@dispatcher.callback_query(F.data == "f2022")
@dispatcher.callback_query(F.data == "f2021")
@dispatcher.callback_query(F.data == "f2020")
@dispatcher.callback_query(F.data == "f2018")
@dispatcher.callback_query(F.data == "f2016")
@dispatcher.callback_query(F.data == "f2014")
@dispatcher.callback_query(F.data == "f2012")
@dispatcher.callback_query(F.data == "f2010")
@dispatcher.callback_query(F.data == "f2005")
@dispatcher.callback_query(F.data == "f2000")
@dispatcher.callback_query(F.data == "f1990")
@dispatcher.callback_query(F.data == "f1980")
@dispatcher.callback_query(F.data == "f1970")
@dispatcher.callback_query(F.data == "f1960")
async def filter_by_year_to(callback):
    year = int(callback.data[1:])
    user_filters[callback.from_user.id].set_year_to(year)
    await filter(callback)

@dispatcher.callback_query(F.data == "random")
async def find_random(callback):
    text_ = "Выполняется поиск ..."
    await callback.message.answer(text=text_)

    movie = get_random_movie()
    while True:
        if (movie['nameRu'] != None):
            break
        movie = get_random_movie()

    image_from_url = URLInputFile(movie['posterUrl'])
    await callback.message.answer_photo(
        image_from_url,
        caption="Постер"
    )
    user_films[callback.from_user.id] = movie['nameRu']
    text__, urls = show_info_about_movie(movie)
    buttons_ = InlineKeyboardBuilder()
    buttons_.add(types.InlineKeyboardButton(text='Kinopoisk', url=urls[0]))
    buttons_.add(types.InlineKeyboardButton(text='Premier', url=urls[1]))
    buttons_.row(types.InlineKeyboardButton(text='Okko', url=urls[2]))
    buttons_.add(types.InlineKeyboardButton(text='Ivi', url=urls[3]))
    buttons_.add(types.InlineKeyboardButton(text='Doramy', url=urls[4]))
    buttons_.row(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='add_in_favourite'))
    await callback.message.answer(text=text__, reply_markup=buttons_.as_markup())


@dispatcher.callback_query(F.data == "new")
async def find_new(callback):
    text_ = "Выполняется поиск ..."
    await callback.message.answer(text=text_)

    movie = get_new_movie()
    while True:
        if (movie['nameRu'] != None):
            break
        movie = get_new_movie()

    image_from_url = URLInputFile(movie['posterUrl'])
    await callback.message.answer_photo(
        image_from_url,
        caption="Постер"
    )
    user_films[callback.from_user.id] = movie['nameRu']
    text__, urls = show_info_about_movie(movie)
    buttons_ = InlineKeyboardBuilder()
    buttons_.add(types.InlineKeyboardButton(text='Kinopoisk', url=urls[0]))
    buttons_.add(types.InlineKeyboardButton(text='Premier', url=urls[1]))
    buttons_.row(types.InlineKeyboardButton(text='Okko', url=urls[2]))
    buttons_.add(types.InlineKeyboardButton(text='Ivi', url=urls[3]))
    buttons_.row(types.InlineKeyboardButton(text='Doramy', url=urls[4]))
    buttons_.row(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='add_in_favourite'))
    await callback.message.answer(text=text__, reply_markup=buttons_.as_markup())

@dispatcher.callback_query(F.data == "popular")
async def find_random(callback):
    text_ = "Выполняется поиск ..."
    await callback.message.answer(text=text_)

    movie = get_random_movie()
    while True:
        if (movie['nameRu'] != None):
            break
        movie = get_popular_movie()

    image_from_url = URLInputFile(movie['posterUrl'])
    await callback.message.answer_photo(
        image_from_url,
        caption="Постер"
    )
    user_films[callback.from_user.id] = movie['nameRu']
    text__, urls = show_info_about_movie(movie)
    buttons_ = InlineKeyboardBuilder()
    buttons_.add(types.InlineKeyboardButton(text='Kinopoisk', url=urls[0]))
    buttons_.add(types.InlineKeyboardButton(text='Premier', url=urls[1]))
    buttons_.row(types.InlineKeyboardButton(text='Okko', url=urls[2]))
    buttons_.add(types.InlineKeyboardButton(text='Ivi', url=urls[3]))
    buttons_.add(types.InlineKeyboardButton(text='Doramy', url=urls[4]))
    buttons_.row(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='add_in_favourite'))
    await callback.message.answer(text=text__, reply_markup=buttons_.as_markup())

@dispatcher.callback_query(F.data == "confirm")
async def confirm(callback):
    rating_low = user_filters[callback.from_user.id].get_rating_from()
    rating_high = user_filters[callback.from_user.id].get_rating_before()
    year_from = user_filters[callback.from_user.id].get_year_from()
    year_to = user_filters[callback.from_user.id].get_year_to()
    genre = user_filters[callback.from_user.id].get_type()
    country = user_filters[callback.from_user.id].get_country()

    await callback.message.answer('Поиск запущен')

    film = by_filter_get(rating_low, rating_high, year_from, year_to, genre, country)



    if (film) == None:
        await callback.message.answer('Фильмов нет')
        return
    else:
        image_from_url = URLInputFile(film['poster']['url'])
        if (image_from_url != None):
            result = await callback.message.answer_photo(
                image_from_url,
                caption="Постер"
            )

        user_films[callback.from_user.id] = film['name']
        text__, urls = show_info_about_movie2(film)
        buttons_ = InlineKeyboardBuilder()
        buttons_.add(types.InlineKeyboardButton(text='Kinopoisk', url=urls[0]))
        buttons_.add(types.InlineKeyboardButton(text='Premier', url=urls[1]))
        buttons_.row(types.InlineKeyboardButton(text='Okko', url=urls[2]))
        buttons_.add(types.InlineKeyboardButton(text='Ivi', url=urls[3]))
        buttons_.add(types.InlineKeyboardButton(text='Doramy', url=urls[4]))
        buttons_.row(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='add_in_favourite'))
        await callback.message.answer(text=text__, reply_markup=buttons_.as_markup())

@dispatcher.callback_query(F.data == "search")
async def find_random(callback):
    await callback.message.answer("Введите название фильма")
@dispatcher.message()
async def handle_user_input(message: types.Message):
    movie_name = message.text.strip()

    if not movie_name:
        await message.answer("Введите название фильма")
        return
    text_ = f"Ищу {movie_name}..."
    await message.answer(text=text_)
    movie = get_movie_info(movie_name)
    if movie['nameRu'] is not None:
        image_from_url = URLInputFile(movie['posterUrl'])
        await message.answer_photo(
            image_from_url,
            caption="Постер"
        )
        user_films[message.from_user.id] = movie['nameRu']

        text__, urls = show_info_about_movie(movie)
        buttons_ = InlineKeyboardBuilder()
        buttons_.add(types.InlineKeyboardButton(text='Kinopoisk', url = urls[0]))
        buttons_.add(types.InlineKeyboardButton(text='Premier', url=urls[1]))
        buttons_.row(types.InlineKeyboardButton(text='Okko', url=urls[2]))
        buttons_.add(types.InlineKeyboardButton(text='Ivi', url=urls[3]))
        buttons_.add(types.InlineKeyboardButton(text='Doramy', url=urls[4]))
        buttons_.row(types.InlineKeyboardButton(text='Добавить в избранное', callback_data='add_in_favourite'))
        await message.answer(text=text__, reply_markup=buttons_.as_markup())
    else:
        await message.answer("Фильм не найден")

@dispatcher.callback_query(F.data == "add_in_favourite")
async def add_favourite(callback):
    cursor.execute("INSERT INTO movies (user_id, movie) VALUES (?, ?)", (callback.from_user.id, user_films[callback.from_user.id]))
    conn.commit()
    await callback.message.answer(text="Добавлено")
@dispatcher.callback_query(F.data == "clear_favourite")
async def delete_movie(callback):
    delete_movie_from_list(callback.from_user.id)
    await callback.message.answer(text="Очищено")

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())