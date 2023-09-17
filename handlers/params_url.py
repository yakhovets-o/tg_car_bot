from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from keyboards import car_kb
from mysql_db import search_option_db


# регистрация машины FSM
class FSM(StatesGroup):
    car = State()
    min_price = State()
    max_price = State()
    tracking_date = State()
    update_period_min = State()


# обработчик старта FSM
async def FSM_start(message: types.Message):
    await FSM.car.set()
    await message.answer('выберите авто.', reply_markup=car_kb)


# обработчик выхода из машины FSM
async def car_cancel(message: types.Message, state: FSMContext):
    current_sate = await state.get_state()
    if current_sate is None:
        return
    await message.answer('Действие отменено.')
    await state.finish()


# обработчик на не корректный ввод  при выборе авто(любое действие кроме нажатия кнопок)
async def car_message(massage: types.Message):
    await massage.answer(f'🔨 Укажите что то из предложенных вариантов\n'
                         f'Для отмены поиска вызовите команду /break')
    await massage.delete()


# обработчик на выбор авто
async def car_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Лекговое авто':
        async with state.proxy() as data:
            data["cars"] = True
            data["truck_cars"] = False
    if call.data == 'Грузовое авто':
        async with state.proxy() as data:
            data["cars"] = False
            data["truck_cars"] = True
    if call.data == 'Лекговое авто / Грузовое авто':
        async with state.proxy() as data:
            data["cars"] = True
            data["truck_cars"] = True
    cars = 'Выбрано' if data["cars"] else 'Не выбрано'
    truck_cars = 'Выбрано' if data["truck_cars"] else 'Не выбрано'
    await call.message.answer(f'Легковое авто - {cars}\nГрузовое авто - {truck_cars}.')
    await call.message.edit_reply_markup()
    await FSM.next()
    await call.message.answer('💵 Введите минимальную стоимость.')
    await call.answer()


# обработчик мин стоимости
async def car_price_start(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["price_min"] = int(message.text)
            await FSM.next()
            await message.answer('💸 Введите максимальную стоимость. ')

    else:
        await message.answer('Введите целое число')
        await message.delete()


# обработчик макс стоимости
async def car_price_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(data["price_min"]) > int(message.text):
            await message.answer('Максимальная стоимость должна привышать минимальную.')
            await message.delete()
        if not message.text.isdigit():
            await message.answer('Введите целое число.')
            await message.delete()
        if message.text.isdigit() and int(data['price_min']) <= int(message.text):
            data["price_max"] = int(message.text)
            await FSM.next()
            await message.answer('📅 Укажите дату  с которой будут отслеживаться публикации',
                                 reply_markup=await DialogCalendar().start_calendar())


# обработчик на не корректный ввод  при выборе авто(любое действие кроме нажатия кнопок)
async def car_publication(massage: types.Message):
    await massage.answer(f'🔨 Укажите что то из предложенных вариантов\n'
                         f'Для отмены поиска вызовите команду /break')
    await massage.delete()


# обработчик периода
async def car_tracking_date(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(call, callback_data)
    if selected:
        async with state.proxy() as data:
            data["tracking_time"] = date.strftime('%Y-%m-%d %H:%M:%S')
            await call.answer()
            await call.message.answer(f'Дата: {data["tracking_time"]}')
            await FSM.next()
            await call.message.answer('⏰ Введите период  обновления  в минутах')


async def update_period_min(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите целое число')
        await message.delete()
    else:
        async with state.proxy() as data:

            data["update_period_min"] = int(message.text)
            data["user_id"] = message.from_user.id
            cars = 'Выбрано' if data["cars"] else 'Не выбрано'
            truck_cars = 'Выбрано' if data["truck_cars"] else 'Не выбрано'
            await message.answer(f'Критерии поиска:\n'
                                 f'Вы выбрали:\n'
                                 f'Лекговое авто - 🚗 {cars}\n'
                                 f'Грузовое авто - 🚚 {truck_cars}\n'
                                 f'Минимальная стоимость 💵 {data["price_min"]} usd\n'
                                 f'Максимальная стоимость 💸 {data["price_max"]} usd\n'
                                 f'Период публикации с 📅 {data["tracking_time"]}\n'
                                 f'Период обновления ⏰ {data["update_period_min"]} min\n\n'
                                 f'Для получения результата вызовите команду /get \n\n'
                                 f'Для изменения параметров поиска вызовите команду /begin'
                                 )

        await search_option_db.option_insert_table(state)
        await state.finish()


# фунция регистрации handlers
def register_handlers_params(dp: Dispatcher):
    dp.register_message_handler(FSM_start, commands='begin', state=None)
    dp.register_message_handler(car_cancel, state="*", commands='break')
    dp.register_message_handler(car_cancel, Text(equals='break', ignore_case=True), state="*")
    dp.register_message_handler(car_message, state=FSM.car)
    dp.register_callback_query_handler(car_choice, Text(endswith='авто'), state=FSM.car)
    dp.register_message_handler(car_price_start, state=FSM.min_price)
    dp.register_message_handler(car_price_finish, state=FSM.max_price)
    dp.register_message_handler(car_publication, state=FSM.tracking_date)
    dp.register_callback_query_handler(car_tracking_date, dialog_cal_callback.filter(), state=FSM.tracking_date)
    dp.register_message_handler(update_period_min, state=FSM.update_period_min)
