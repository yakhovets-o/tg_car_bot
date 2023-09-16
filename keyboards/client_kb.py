from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# клавиатура появляется во время обработчика  на выбор авто
car_kb = InlineKeyboardMarkup(row_width=2)
car_kb.add(InlineKeyboardButton(text='🚗 Лекговое авто', callback_data='Лекговое авто'),
             InlineKeyboardButton(text='🚚 Грузовое авто', callback_data='Грузовое авто'),
             InlineKeyboardButton(text='🚗 Лекговое авто / 🚚 Грузовое авто',
                                  callback_data='Лекговое авто / Грузовое авто')
             )


