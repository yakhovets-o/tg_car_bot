import time
import json
import requests
from datetime import datetime, timedelta
from mysql_db.kufar_db import kuf_insert_table


# фун-ция для получения url
def get_url(price_min, price_max, view_machine, user_id):
    cookies = {
        'lang': 'ru',
        'rl_session': 'RudderEncrypt^%^3AU2FsdGVkX18^%^2BtT^%^2BFyZWv4nzkpa8Ww65xY2py^%^2BERfw5xdDiHDuNu2HZGKcCIEN2jCey9Rx6FBSOROZBGysuQEksNFKVkcqA2z4G4qk9ucr7rU3fXKFH3YFNRazMKVkCjXL9wbyiR8uzl6hsvJ9lz6ow^%^3D^%^3D',
        'rl_user_id': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FWN9sowwSYfcyNy^%^2BKNmvseq9EzMOGQHe0^%^3D',
        'rl_trait': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FITwdkaVq5yC2B^%^2BWlM7Amm^%^2FCbQakJsyfs^%^3D',
        'rl_group_id': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2BEEbYzOyR0^%^2FyNg^%^2B9BxKa03fFD0YeJ60ag^%^3D',
        'rl_group_trait': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2Ffi4x9dlHP7yjqJZd3ZAyjBwm3JdVyP^%^2Bs^%^3D',
        'rl_anonymous_id': 'RudderEncrypt^%^3AU2FsdGVkX18XXnajMMRVkV7veRoglcVPoWtAm1YT^%^2BHm6Bg7ym447cFQfKC^%^2Bqm8q7hfQwdENGAok279ECXwwX0g^%^3D^%^3D',
        'rl_page_init_referrer': 'RudderEncrypt^%^3AU2FsdGVkX1^%^2FBz^%^2FyZ2m8uvvocKht037Dsv0uvDDy9NCN02G0lqMC^%^2BEUKvzRju40bs',
        'rl_page_init_referring_domain': 'RudderEncrypt^%^3AU2FsdGVkX189FjPjp8epCB3WBKetTBl5Xy^%^2BYU3T7QpCPxFBAI7R7ZLZSP1gW5X^%^2Fp',
        '_ga': 'GA1.2.214778382.1689607879',
        'kuf_agr': '{^%^22advertisements^%^22:true^%^2C^%^22statistic^%^22:true^%^2C^%^22mindbox^%^22:true}',
        'fullscreen_cookie': '1',
        '_gcl_au': '1.1.2009610434.1689607886',
        '_ga_QTFZM0D0BE': 'GS1.1.1693178836.7.1.1693179263.60.0.0',
        '_hjSessionUser_2040951': 'eyJpZCI6ImFlNGE4YTk0LTc0NTQtNTY3Yy1hNTkzLWFlODJmYTNiMzE1MCIsImNyZWF0ZWQiOjE2ODk2MDc4ODc0NTQsImV4aXN0aW5nIjp0cnVlfQ==',
        'tmr_lvid': 'c0b96724852b44284334629446be9d1a',
        'tmr_lvidTS': '1689607887498',
        '_fbp': 'fb.1.1689607889034.560600361',
        '__gads': 'ID=b6e08b6691b2d272:T=1689607867:RT=1694421380:S=ALNI_MZKt-llxOSeOKaXBa06o7bCegWzzw',
        '__gpi': 'UID=00000c6a5b4c38bb:T=1689607867:RT=1694421380:S=ALNI_MbIkSN_GZFVcs3OZWnxCBGwigaWvw',
        'mindboxDeviceUUID': '3473b177-ee14-4699-a228-e67eefd774ca',
        'directCrm-session': '^%^7B^%^22deviceGuid^%^22^%^3A^%^223473b177-ee14-4699-a228-e67eefd774ca^%^22^%^7D',
        '_ga_WLP2F7MG5H': 'GS1.1.1694421391.11.1.1694421417.34.0.0',
        'kuf_SA_subscribe_user_attention': '1',
        'kuf_VCH_promo_vas': '1',
        'web_push_banner_listings': '2',
        'kufar_cart_id': '5f76f901-e227-4449-be5c-98798acd1228',
        'web_push_banner_auto': '3',
        '_gid': 'GA1.2.350782272.1694421388',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': 'lang=ru; rl_session=RudderEncrypt^%^3AU2FsdGVkX18^%^2BtT^%^2BFyZWv4nzkpa8Ww65xY2py^%^2BERfw5xdDiHDuNu2HZGKcCIEN2jCey9Rx6FBSOROZBGysuQEksNFKVkcqA2z4G4qk9ucr7rU3fXKFH3YFNRazMKVkCjXL9wbyiR8uzl6hsvJ9lz6ow^%^3D^%^3D; rl_user_id=RudderEncrypt^%^3AU2FsdGVkX1^%^2FWN9sowwSYfcyNy^%^2BKNmvseq9EzMOGQHe0^%^3D; rl_trait=RudderEncrypt^%^3AU2FsdGVkX1^%^2FITwdkaVq5yC2B^%^2BWlM7Amm^%^2FCbQakJsyfs^%^3D; rl_group_id=RudderEncrypt^%^3AU2FsdGVkX1^%^2BEEbYzOyR0^%^2FyNg^%^2B9BxKa03fFD0YeJ60ag^%^3D; rl_group_trait=RudderEncrypt^%^3AU2FsdGVkX1^%^2Ffi4x9dlHP7yjqJZd3ZAyjBwm3JdVyP^%^2Bs^%^3D; rl_anonymous_id=RudderEncrypt^%^3AU2FsdGVkX18XXnajMMRVkV7veRoglcVPoWtAm1YT^%^2BHm6Bg7ym447cFQfKC^%^2Bqm8q7hfQwdENGAok279ECXwwX0g^%^3D^%^3D; rl_page_init_referrer=RudderEncrypt^%^3AU2FsdGVkX1^%^2FBz^%^2FyZ2m8uvvocKht037Dsv0uvDDy9NCN02G0lqMC^%^2BEUKvzRju40bs; rl_page_init_referring_domain=RudderEncrypt^%^3AU2FsdGVkX189FjPjp8epCB3WBKetTBl5Xy^%^2BYU3T7QpCPxFBAI7R7ZLZSP1gW5X^%^2Fp; _ga=GA1.2.214778382.1689607879; kuf_agr={^%^22advertisements^%^22:true^%^2C^%^22statistic^%^22:true^%^2C^%^22mindbox^%^22:true}; fullscreen_cookie=1; _gcl_au=1.1.2009610434.1689607886; _ga_QTFZM0D0BE=GS1.1.1693178836.7.1.1693179263.60.0.0; _hjSessionUser_2040951=eyJpZCI6ImFlNGE4YTk0LTc0NTQtNTY3Yy1hNTkzLWFlODJmYTNiMzE1MCIsImNyZWF0ZWQiOjE2ODk2MDc4ODc0NTQsImV4aXN0aW5nIjp0cnVlfQ==; tmr_lvid=c0b96724852b44284334629446be9d1a; tmr_lvidTS=1689607887498; _fbp=fb.1.1689607889034.560600361; __gads=ID=b6e08b6691b2d272:T=1689607867:RT=1694421380:S=ALNI_MZKt-llxOSeOKaXBa06o7bCegWzzw; __gpi=UID=00000c6a5b4c38bb:T=1689607867:RT=1694421380:S=ALNI_MbIkSN_GZFVcs3OZWnxCBGwigaWvw; mindboxDeviceUUID=3473b177-ee14-4699-a228-e67eefd774ca; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^223473b177-ee14-4699-a228-e67eefd774ca^%^22^%^7D; _ga_WLP2F7MG5H=GS1.1.1694421391.11.1.1694421417.34.0.0; kuf_SA_subscribe_user_attention=1; kuf_VCH_promo_vas=1; web_push_banner_listings=2; kufar_cart_id=5f76f901-e227-4449-be5c-98798acd1228; web_push_banner_auto=3; _gid=GA1.2.350782272.1694421388',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    u = f"https://api.kufar.by/search-api/v1/search/rendered-paginated?prc=r%3A{price_min}%2C{price_max}"
    for view in view_machine:
        params = {
            'cat': {view},
            'cur': 'USD',
            'lang': 'ru',
            'size': 50,
            'sort': 'lst.d',
            'typ': 'sell'

        }
        url = requests.get(url=u, cookies=cookies, headers=headers, params=params)
        time.sleep(3)
        ads = url.json()
        with open(fr'parsers/kufar_ads/{user_id}_{view}.json', 'w', encoding='utf-8') as file:
            json.dump(ads, file, indent=4, ensure_ascii=False)
        print('получение урл', url.url)


# фун-ция получения адреса объявления
def get_link(auto) -> str:
    return auto['ad_link']


# фун-ция получения параметров авто
def get_params(auto) -> dict:
    params = {'Марка': 'Не указано', 'Модель': 'Не указано', 'Год': 'Не указано', 'Тип двигателя': 'Не указано',
              'Объем, л': 'Не указано', 'Область': 'Не указано', 'Город / Район': 'Не указано'}

    for param in auto['ad_parameters']:
        if param['pl'] in params:
            params[param['pl']] = param['vl']
    return params


# фун-ция получения объекта даты подачи объявления
def get_date(auto) -> datetime:
    date_str = datetime.strftime(datetime.fromisoformat(auto['list_time'][:-1]), '%Y-%m-%d %H:%M:%S')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)
    return date_obj


# фун-ция получения стоимости в usd
def get_price_usd(auto) -> int:
    usd_str = auto['price_usd']
    usd_price = int(usd_str[:-2] if len(usd_str) > 2 else 0)
    return usd_price


# фун-ция получения стоимости в byn
def get_price_byn(auto) -> int:
    byn_str = auto['price_byn']
    byn_price = int(byn_str[:-2] if len(byn_str) > 2 else 0)
    return byn_price


# заргузка всех параметров и бд
def load_param_in_db(view_machine, user_id, tracing_data):
    for view in view_machine:
        with open(fr'parsers/kufar_ads/{user_id}_{view}.json', 'r', encoding='utf-8') as file:
            cars = json.load(file)
            for car in cars['ads']:
                # условие если время объявления больше времени с которого начался отбор и если объявления нет в таблице
                # в которой хранятся объявления которые уже были отправлены пользователю
                if get_date(car) > tracing_data:
                    all_params = (
                        user_id, *get_params(car).values(), get_price_usd(car), get_price_byn(car), get_link(car),
                        get_date(car),)
                    kuf_insert_table(all_params)
                else:
                    break
