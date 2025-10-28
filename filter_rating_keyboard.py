from aiogram.utils.keyboard import InlineKeyboardBuilder

keyboard_builder = InlineKeyboardBuilder()
keyboard_builder.button(text=str(10), callback_data='ten')
keyboard_builder.button(text=str(9), callback_data='nine')
keyboard_builder.button(text=str(8), callback_data='eight')
keyboard_builder.button(text=str(7), callback_data='seven')
keyboard_builder.button(text=str(6), callback_data='six')
keyboard_builder.button(text=str(5), callback_data='five')
keyboard_builder.button(text=str(4), callback_data='four')
keyboard_builder.button(text=str(3), callback_data='three')
keyboard_builder.button(text=str(2), callback_data='two')
keyboard_builder.button(text=str(1), callback_data='one')
keyboard_builder.button(text=str(0), callback_data='zero')
keyboard_builder.adjust(4,3,4)

keyboard_builder2 = InlineKeyboardBuilder()
keyboard_builder2.button(text=str(10), callback_data='ten2')
keyboard_builder2.button(text=str(9), callback_data='nine2')
keyboard_builder2.button(text=str(8), callback_data='eight2')
keyboard_builder2.button(text=str(7), callback_data='seven2')
keyboard_builder2.button(text=str(6), callback_data='six2')
keyboard_builder2.button(text=str(5), callback_data='five2')
keyboard_builder2.button(text=str(4), callback_data='four2')
keyboard_builder2.button(text=str(3), callback_data='three2')
keyboard_builder2.button(text=str(2), callback_data='two2')
keyboard_builder2.button(text=str(1), callback_data='one2')
keyboard_builder2.button(text=str(0), callback_data='zero2')
keyboard_builder2.adjust(4,3,4)

rating_from_map = {
    'ten': 10,
    'nine': 9,
    'eight': 8,
    'seven': 7,
    'six': 6,
    'five': 5,
    'four': 4,
    'three': 3,
    'two': 2,
    'one': 1,
    'zero': 0,
}

rating_before_map = {
    'ten2': 10,
    'nine2': 9,
    'eight2': 8,
    'seven2': 7,
    'six2': 6,
    'five2': 5,
    'four2': 4,
    'three2': 3,
    'two2': 2,
    'one2': 1,
    'zero2': 0,
}