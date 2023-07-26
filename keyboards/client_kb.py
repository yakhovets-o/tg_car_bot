from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_town_car = KeyboardButton('🚗 Лекговое авто')
button_truck_car = KeyboardButton('🚚 Грузовое авто')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_kb.row(button_town_car, button_truck_car)