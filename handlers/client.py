from aiogram import types, Dispatcher
from create_bot import admin, support
from other_func import salute, now_time


# обработчик на команду start
async def start_command(message: types.Message):
    your_name = message.from_user.first_name
    await message.answer(f'{salute(now_time)} {your_name} !\n'
                         f'Для указания  параметров поиска вызовите команду /begin')


# обработчик на команду contacts
async def contacts_command(message: types.Message):
    await message.answer(f'Admin {admin}')


# обработчик на команду support
async def support_command(message: types.Message):
    await message.answer(f'Поддержка бота  {support}')


# обработчик на команду sub
async def sub_command(message: types.Message):
    await message.answer(f'На данный момент подписка недоступна')


# обработчик на команду help
async def help_command(message: types.Message):
    await message.answer(f'Полный список команд:\n'
                         f'/start - Запуск бота\n'
                         f'/contacts - Контакты для связи\n'
                         f'/support - Написать в поддержку\n'
                         f'/sub - оплата подписки\n'
                         f'/begin - Параметры поиска'
                         )


# регистрация функции handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(contacts_command, commands=['contacts'])
    dp.register_message_handler(support_command, commands=['support'])
    dp.register_message_handler(sub_command, commands=['sub'])
    dp.register_message_handler(help_command, commands=['help'])
