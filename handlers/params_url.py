import json
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hlink, hbold
from keyboards import start_kb, publ_per_kb
from sqlite_db import db_py
from parser_car import get_url


# регистрация машины FSM
class FSM(StatesGroup):
    car = State()
    min_price = State()
    max_price = State()
    time_publication = State()


# обработчик старта FSM
async def FSM_start(message: types.Message):
    await FSM.car.set()
    await message.answer('выберите авто', reply_markup=start_kb)


# обработчик выхода из машины FSM
async def car_cancel(message: types.Message, state: FSMContext):
    current_sate = await state.get_state()
    if current_sate is None:
        return
    await message.answer('Действие отменено')
    await state.finish()


# обработчик на не корректный ввод  при выборе авто(любое действие кроме нажатия кнопок)
async def car_message(massage: types.Message):
    await massage.answer(f'Укажите что то из предложенных вариантов\n'
                         f'Для отмены поиска вызовите команду /break', reply_markup=start_kb)
    await massage.delete()


# обработчик на выбор авто
async def car_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Лекговое авто':
        async with state.proxy() as data:
            data['cars'] = 'cars'
    if call.data == 'Грузовое авто':
        async with state.proxy() as data:
            data['cars'] = "truck"
    await FSM.next()
    await call.message.answer('введите минимальную стоимость ')
    await call.answer()


# обработчик мин стоимости
async def car_price_start(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['price_usd[min]'] = int(message.text)
            await FSM.next()
            await message.answer('введите максимальную стоимость ')

    else:
        await message.answer('введите целое число')
        await message.delete()


# обработчик макс стоимости
async def car_price_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(data['price_usd[min]']) > int(message.text):
            await message.answer('максимальная стоимость должна привышать минимальную')
            await message.delete()
        if not message.text.isdigit():
            await message.answer('введите целое число')
            await message.delete()
        if message.text.isdigit() and int(data['price_usd[min]']) <= int(message.text):
            data['price_usd[max]'] = int(message.text)
            await FSM.next()
            await message.answer('Укажите период публикации', reply_markup=publ_per_kb)


# обработчик на не корректный ввод  при выборе авто(любое действие кроме нажатия кнопок)
async def car_publication(massage: types.Message):
    await massage.answer(f'Укажите что то из предложенных вариантов\n'
                         f'Для отмены поиска вызовите команду /break', reply_markup=publ_per_kb)
    await massage.delete()


# обработчик периода
async def car_time_publication(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Сегодня':
        async with state.proxy() as data:
            data['publ'] = 10
    if call.data == '2 дня':
        async with state.proxy() as data:
            data['publ'] = 11
    if call.data == '3 дня':
        async with state.proxy() as data:
            data['publ'] = 12
    if call.data == '4 дня':
        async with state.proxy() as data:
            data['publ'] = 13
    if call.data == 'Неделя':
        async with state.proxy() as data:
            data['publ'] = 16
    if call.data == 'Любой':
        async with state.proxy() as data:
            data['publ'] = ''
    async with state.proxy() as data:
        data['id'] = call.from_user.id
    await call.message.answer(f'Критерии поиска:\n'
                              f'Вы выбрали {data["cars"]}\n'
                              f'Минимальная сумма {data["price_usd[min]"]} usd\n'
                              f'Максимальная сумма {data["price_usd[max]"]} usd\n'
                              f'Период публикации {call.data}\n'
                              f'Для получения результата нажмите /get '
                              )
    await call.answer()
    await db_py.db_add_command(state)
    await state.finish()


# сбор параметов поиска окончен
# получение результов поиска

async def get_car(message: types.Message):
    await message.answer('Пожалуйста подождите...')
    # вызов парсера
    get_url()
    id = message.from_user.id
    with open(rf'C:\Users\lego\PycharmProjects\car_bot\cars_users\{id}.json', mode='r', encoding='utf-8') as file:
        value = json.load(file)
        if len(value) > 0:
            for item in value:
                await asyncio.sleep(1)
                card = f'{hlink(item["car_name"], item["car_url"])}\n' \
                       f'{hbold("Цена: ")} {item["price_car_usd"]}, {item["price_car_byn"]}\n' \
                       f'{hbold("Год: ")} {item["param_car"]}\n' \
                       f'{hbold("Дата и место: ")} {item["data_car"]}, {item["city_car"]}'
                await message.answer(card)
                await message.answer('Поиск окончен')
            # обнуление json файла
            with open(rf'C:\Users\lego\PycharmProjects\car_bot\cars_users\{id}.json', 'w') as file:
                pass
            # удаление параметров из бд (что бы не было сохранений нескольких параметров из одного id)
            await db_py.db_del_user(id)
        else:
            await message.answer('Объявлений обнаружено не было')


# результат получен
# фунция регистрации handlers
def register_handlers_params(dp: Dispatcher):
    dp.register_message_handler(FSM_start, commands='begin', state=None)
    dp.register_message_handler(car_cancel, state="*", commands='break')
    dp.register_message_handler(car_cancel, Text(equals='break', ignore_case=True), state="*")
    dp.register_message_handler(car_message, state=FSM.car)
    dp.register_callback_query_handler(car_choice, Text(endswith='авто'), state=FSM.car)
    dp.register_message_handler(car_price_start, state=FSM.min_price)
    dp.register_message_handler(car_price_finish, state=FSM.max_price)
    dp.register_message_handler(car_publication, state=FSM.time_publication)
    dp.register_callback_query_handler(car_time_publication, state=FSM.time_publication)
    dp.register_message_handler(get_car, commands='get')
