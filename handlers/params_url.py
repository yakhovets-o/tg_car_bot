import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboards import start_kb


class FSM(StatesGroup):
    car = State()
    min_price = State()
    max_price = State()
    time = State()


async def FSM_start(message: types.Message):
    await FSM.car.set()
    await message.answer('выберите авто', reply_markup=start_kb)


async def car_cancel(message: types.Message, state: FSMContext):
    current_sate = await state.get_state()
    if current_sate is None:
        return
    await message.answer('Действие отменено')
    await state.finish()


async def car_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Лекговое авто':
        async with state.proxy() as data:
            data['cars'] = 'Лекговое авто'
    if call.data == 'Грузовое авто':
        async with state.proxy() as data:
            data['cars'] = "Грузовое авто"
    await FSM.next()
    await call.message.answer('введите минимальную стоимость ')
    await call.answer()


async def car_price_start(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['filter?price_usd[min]='] = message.text
            await FSM.next()
            await message.answer('введите максимальную стоимость ')

    else:
        await message.answer('введите целое число')


async def car_price_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(data['filter?price_usd[min]=']) > int(message.text):
            await message.answer('максимальная стоимость должна привышать минимальную')
        if not message.text.isdigit():
            await message.answer('введите целое число')
        if message.text.isdigit() and int(data['filter?price_usd[min]=']) <= int(message.text):
            data['&price_usd[max]='] = message.text
            await FSM.next()
            await message.answer('введите время начала работы, в формате hh (часы):mm (минуты)')


async def car_time(message: types.Message, state: FSMContext):
    if bool(re.fullmatch(r'([0-1][0-9]|2[0-3]):[0-5][0-9]', message.text)):
        async with state.proxy() as data:
            data['time'] = message.text
            await message.answer(f'Критерии поиска:\n'
                                 f'Вы выбрали {data["cars"]}\n'
                                 f'Минимальная сумма {data["filter?price_usd[min]="]} usd\n'
                                 f'Максимальная сумма {data["&price_usd[max]="]} usd\n'
                                 f'Обновления будут поступать с {data["time"]}\n'
                                 )
    else:
        await message.answer('Некорректно указано время')
    async with state.proxy() as data:
        params = dict(data)
    await state.finish()


def register_handlers_params(dp: Dispatcher):
    dp.register_message_handler(FSM_start, commands='begin', state=None)
    dp.register_message_handler(car_cancel, state="*", commands='break')
    dp.register_message_handler(car_cancel, Text(equals='break', ignore_case=True), state="*")
    dp.register_callback_query_handler(car_choice, Text(endswith='авто'), state=FSM.car)
    dp.register_message_handler(car_price_start, state=FSM.min_price)
    dp.register_message_handler(car_price_finish, state=FSM.max_price)
    dp.register_message_handler(car_time, state=FSM.time)
