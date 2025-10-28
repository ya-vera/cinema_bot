from aiogram.utils.keyboard import InlineKeyboardBuilder

keyboard_builder3 = InlineKeyboardBuilder()
keyboard_builder3.button(text='ВСЕ', callback_data='all')
keyboard_builder3.button(text='Россия', callback_data='Russia')
keyboard_builder3.button(text='США', callback_data='USA')
keyboard_builder3.button(text='Китай', callback_data='China')
keyboard_builder3.button(text='Южная Корея', callback_data='SK')
keyboard_builder3.button(text='Великобритания', callback_data='UK')
keyboard_builder3.button(text='Канада', callback_data='Canada')
keyboard_builder3.button(text='Испания', callback_data='Spain')
keyboard_builder3.button(text='Италия', callback_data='Italy')
keyboard_builder3.button(text='Франция', callback_data='France')
keyboard_builder3.button(text='Германия', callback_data='Germany')
keyboard_builder3.button(text='Индия', callback_data='India')
keyboard_builder3.button(text='Турция', callback_data='Turkey')
keyboard_builder3.button(text='Бельгия', callback_data='Belgium')
keyboard_builder3.button(text='Аргентина', callback_data='Argentina')
keyboard_builder3.button(text='Австрия', callback_data='Austria')
keyboard_builder3.adjust(1,3,2,3,2,3,2)

country_map = {
    'all': 'ВСЕ',
    'Russia': 'Россия',
    'USA': 'США',
    'China': 'Китай',
    'SK': 'Южная Корея',
    'UK': 'Великобритания',
    'Canada': 'Канада',
    'Spain': 'Испания',
    'Italy': 'Италия',
    'France': 'Франция',
    'Germany': 'Германия',
    'India': 'Индия',
    'Turkey': 'Турция',
    'Belgium': 'Бельгия',
    'Argentina': 'Аргентина',
    'Austria': 'Австрия'
}