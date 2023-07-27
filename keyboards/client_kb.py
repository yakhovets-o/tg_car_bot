from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(row_width=2)
start_kb.add(InlineKeyboardButton(text='🚗 Лекговое авто', callback_data='Лекговое авто'),
             InlineKeyboardButton(text='🚚 Грузовое авто', callback_data='Грузовое авто'))
