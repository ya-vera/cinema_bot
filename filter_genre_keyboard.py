from aiogram.utils.keyboard import InlineKeyboardBuilder

keyboard_builder4 = InlineKeyboardBuilder()
keyboard_builder4.button(text='ВСЕ', callback_data='all2')
keyboard_builder4.button(text='Биографический', callback_data='biographical')
keyboard_builder4.button(text='Фантастика', callback_data='fantasy')
keyboard_builder4.button(text='Боевик', callback_data='action')
keyboard_builder4.button(text='Вестерн', callback_data='western')
keyboard_builder4.button(text='Военный', callback_data='military')
keyboard_builder4.button(text='Детектив', callback_data='detective')
keyboard_builder4.button(text='Детский', callback_data='child')
keyboard_builder4.button(text='Документальный', callback_data='documentary')
keyboard_builder4.button(text='Драма', callback_data='drama')
keyboard_builder4.button(text='Комедия', callback_data='comedy')
keyboard_builder4.button(text='Криминал', callback_data='crime')
keyboard_builder4.button(text='Ужасы', callback_data='horrors')
keyboard_builder4.button(text='Мелодрама', callback_data='melodrama')
keyboard_builder4.button(text='Мультфильм', callback_data='cartoon')
keyboard_builder4.button(text='Мюзикл', callback_data='musical')
keyboard_builder4.button(text='Приключения', callback_data='adventures')
keyboard_builder4.button(text='Семейный', callback_data='family')
keyboard_builder4.button(text='Спорт', callback_data='sport')
keyboard_builder4.button(text='Триллер', callback_data='thriller')
keyboard_builder4.adjust(1,2,3,2,2,3,2,2,3)

genre_map = {
    'all2': 'ВСЕ',
    'biographical': 'Биографический',
    'fantasy': 'Фантастика',
    'action': 'Боевик',
    'western': 'Вестерн',
    'military': 'Военный',
    'detective': 'Детектив',
    'child': 'Детский',
    'documentary': 'Документальный',
    'drama': 'Драма',
    'comedy': 'Комедия',
    'crime': 'Криминал',
    'horrors': 'Ужасы',
    'melodrama': 'Мелодрама',
    'cartoon': 'Мультфильм',
    'musical': 'Мюзикл',
    'adventures':' Приключения',
    'family': 'Семейный',
    'sport': 'Спорт',
    'thriller': 'Триллер'
}