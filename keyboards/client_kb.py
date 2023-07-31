from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# клавиатура появляется во время обработчика  на выбор авто
start_kb = InlineKeyboardMarkup(row_width=2)
start_kb.add(InlineKeyboardButton(text='🚗 Лекговое авто', callback_data='Лекговое авто'),
             InlineKeyboardButton(text='🚚 Грузовое авто', callback_data='Грузовое авто')
             )
# клавиатура появляется во время обработчика  на выбор периода
publ_per_kb = InlineKeyboardMarkup(row_width=3)
publ_per_kb.add(InlineKeyboardButton(text='За сегодня ', callback_data='Сегодня'),
                InlineKeyboardButton(text='За 2 дня', callback_data='2 дня'),
                InlineKeyboardButton(text='За 3 дня', callback_data='3 дня'),
                InlineKeyboardButton(text='За 4 дня', callback_data='4 дня'),
                InlineKeyboardButton(text='За неделю', callback_data='Неделя'),
                InlineKeyboardButton(text='Любой', callback_data='Любой')
                )
