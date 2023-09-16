import asyncio
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hlink, hbold
from mysql_db import kufar_db, av_db, vk_db, search_option_db
from parsers import kufar_parser, av_parser, vk_parser


async def get_ready_ads(message: types.Message):
    await message.answer('Пожалуйста подождите...')
    us_id = message.from_user.id

    while True:

        # параментры для url запроса kufar
        # делаем запрос в бд и сохраняем параметры по которым будет искать авто в переменную по used_id отправителя
        search_param = search_option_db.option_select_table(user_id=us_id)

        # cars  легковые авто(True) тогда пользователь выбрал его (False) нет
        # truck_cars  аналогично как и с cars
        # price_min минимальная цена авто
        # price_max максимальная дата авто
        # tracing_data  дата с которого начанается отбор объявлений
        # update_period_min периодичность к которой пользователь будет получать апдейты
        cars, truck_cars, price_min, price_max, tracing_data, update_period_min, user_id = search_param[0]

        # 2010(легковое авто) и 2060(грузовое авто) коды по которым открывается раздел с легковым и грузовым авто
        kufar_view_machine = [2010 if cars else None, 2060 if truck_cars else None]
        kufar_view_machine = [i for i in kufar_view_machine if i]

        # cars(легковое авто) и truck(грузовое авто) коды по которым открывается раздел с легковым и грузовым авто
        av_view_machine = ['cars' if cars else None, 'truck' if truck_cars else None]
        av_view_machine = [i for i in av_view_machine if i]

        # вызов фун-ций парсера
        # вызов фун-ции которая получает урл для парсера kufar и записывает в json файл
        kufar_parser.get_url(price_min=price_min, price_max=price_max, view_machine=kufar_view_machine, user_id=user_id)

        # фун-ция проходит по полученным урл и собирает нужные данные и закидывает в бд
        kufar_parser.load_param_in_db(view_machine=kufar_view_machine, user_id=user_id, tracing_data=tracing_data)

        # выгружаем данные из бд и сохраняем в переменную
        kuf_posts = kufar_db.kuf_select_table(user_id=user_id)

        # после сохранения данных в переменную очищаем таблицу
        kufar_db.kuf_del_table(user_id=user_id)

        for post in kuf_posts:
            us_id, brand, model, year_production, engine_type, engine_volume, region, city, price_usd, price_byn, \
                link, date_time_post, data_now = post
            await asyncio.sleep(3)
            try:
                card = f'{hbold("Модель и марка: ")} {hlink((brand + " " + model), link)}\n' \
                       f'{hbold("Год: ")} {year_production}\n' \
                       f'{hbold("Тип двигателя и объем: ")} {engine_type}, {engine_volume}\n' \
                       f'{hbold("Дата публикации и место: ")}  {date_time_post}, {region}  {city}\n' \
                       f'{hbold("Цена: ")} {price_usd} Br ≈ {price_byn} Usd'
                await message.answer(card)
            except Exception as ex:
                print(ex)
                continue

        # фун- ция получает урл проходит по ним собирает нужные объявления и закидывает в бд
        av_parser.get_post(price_min=price_min, price_max=price_max, view_machine=av_view_machine,
                           tracing_data=tracing_data, user_id=user_id)

        # выгружаем данные из бд и сохраняем в переменную
        av_posts = av_db.av_select_table(user_id=user_id)

        # после сохранения данных в переменную очищаем таблицу
        av_db.av_del_table(user_id=user_id)

        for post in av_posts:
            us_id, brand, model, year, engine_type, engine_capacity, cond, region, city, price_byn, price_usd, link, \
                date_time_post, data_now = post
            card = f'{hbold("Модель и марка: ")} {hlink((brand + " " + model), link)}\n' \
                   f'{hbold("Состояние: ")} {cond}\n' \
                   f'{hbold("Год: ")} {year}\n' \
                   f'{hbold("Тип двигателя и объем: ")} {engine_type}, {engine_capacity}\n' \
                   f'{hbold("Дата публикации и место: ")}  {date_time_post}, {region}  {city}\n' \
                   f'{hbold("Цена: ")} {price_usd} Br ≈ {price_byn} Usd'
            await message.answer(card)

        # фун-ция делает  get запрос результат сохранает в json
        vk_parser.get_json(user_id=user_id)

        # фун-ция пробегается по json файлам и отбирает посты по критериям
        vk_parser.get_post(user_id=user_id, tracing_data=tracing_data, price_max=price_max)

        # выгружаем данные из бд и сохраняем в переменную
        vk_posts = vk_db.vk_select_table(user_id=user_id)

        # после сохранения данных в переменную очищаем таблицу
        vk_db.vk_del_table(user_id=user_id)

        for post in vk_posts:
            us_id, link_post, link_user, body_post, date_time_post, data_now = post
            card = f'{hbold("Пост: ")} {link_post}\n' \
                   f'{hbold("Владелец поста: ")} {link_user}\n' \
                   f'{hbold("Описание: ")} {body_post}\n' \
                   f'{hbold("Дата поста: ")} {date_time_post}'
            await message.answer(card)

        # функция обновления времени поиска для чтобы парсинг не начинался каджый раз с той даты которую указал
        # пользователь
        search_option_db.option_update_table(time=datetime.now(), user_id=user_id)
        # засыпаем на тот период коготорый указал пользователь
        await asyncio.sleep(update_period_min * 60)


def register_handlers_kuf_pars(dp: Dispatcher):
    dp.register_message_handler(get_ready_ads, commands='get')
