from aiogram import types, Dispatcher


# обработчик на на неустановленные команды
async def mess_other(message: types.Message):
    await message.answer(f'Команда некорректна\n'
                         f'Список команд можно получить по команде /help')
    await message.delete()


# регистрация  функции handler
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(mess_other)
