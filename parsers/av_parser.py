import time
import requests
from datetime import datetime, timedelta
from mysql_db import av_db


# фун-ция получения времени публикации
def get_time_post(time_post) -> datetime:
    time_publ_obj = datetime.strptime(time_post.replace('T', ' ').replace('+0000', ''), '%Y-%m-%d %H:%M:%S') \
                    + timedelta(hours=3)
    return time_publ_obj


# фун-ция получения параметров авто
def get_params(auto) -> dict:
    params = {'brand': 'Не указано', 'model': 'Не указано', 'year': 'Не указано', 'engine_type': 'Не указано',
              'engine_capacity': 'Не указано', 'condition': 'Не указано'}

    for prop in auto['properties']:
        if prop['name'] in params:
            params[prop['name']] = prop['value']
    return params


# фун-ция получения постов с авто
def get_post(price_min, price_max, view_machine, tracing_data, user_id):
    print(tracing_data)
    cookies = {
        '_ga_GWM6BXJZNK': 'GS1.1.1690553021.5.1.1690553137.0.0.0',
        '_ga': 'GA1.1.115487787.1689690249',
        '_fbp': 'fb.1.1689690251208.2043510689',
        'acceptedCookies': '{^%^22accepted^%^22:true^%^2C^%^22analytical^%^22:true^%^2C^%^22technical^%^22:true^%^2C^%^22promotion^%^22:true}',
        '__gads': 'ID=2f7ef2b02daf11f3:T=1689690242:RT=1690552996:S=ALNI_MYjr0kOFw_JeBHcLtBsMWvtNdvQvQ',
        '__gpi': 'UID=00000c3ed84f8078:T=1689690242:RT=1690552996:S=ALNI_MaAWqGaqL35NpyrVXxN9vpOzdxV4w',
        '_gcl_au': '1.1.1244413043.1689690548',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga_GWM6BXJZNK=GS1.1.1690553021.5.1.1690553137.0.0.0; _ga=GA1.1.115487787.1689690249; _fbp=fb.1.1689690251208.2043510689; acceptedCookies={^%^22accepted^%^22:true^%^2C^%^22analytical^%^22:true^%^2C^%^22technical^%^22:true^%^2C^%^22promotion^%^22:true}; __gads=ID=2f7ef2b02daf11f3:T=1689690242:RT=1690552996:S=ALNI_MYjr0kOFw_JeBHcLtBsMWvtNdvQvQ; __gpi=UID=00000c3ed84f8078:T=1689690242:RT=1690552996:S=ALNI_MaAWqGaqL35NpyrVXxN9vpOzdxV4w; _gcl_au=1.1.1244413043.1689690548',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    params = {'price_usd[min]': price_min, 'price_usd[max]': price_max, 'sort': 4}
    for view in view_machine:
        url = f'https://api.av.by/offer-types/{view}/filters/main/init?'
        try:
            request = requests.get(url=url, headers=headers, params=params, cookies=cookies)
            response = request.json()
            big_url = request.url
            print(big_url)
            page = 1
            try:
                # проходим все стр с объявлениями
                while page < int(response['pageCount']) + 1:
                    page_url = requests.get(url=big_url, headers=headers, params={'page': page}, cookies=cookies)
                    time.sleep(5)
                    car = page_url.json()
                    for auto in car['adverts']:
                        # условие если время объявления больше времени с которого начался отбор и если объявления нет в таблице
                        # в которой хранятся объявления которые уже были отправлены пользователю
                        if get_time_post(auto['publishedAt']) > tracing_data:
                            region = auto['locationName']
                            city = auto['shortLocationName']
                            price_car_byn = auto['price']['byn']['amount']
                            price_car_usd = auto['price']['usd']['amount']
                            link = auto['publicUrl']

                            all_params = (user_id, *get_params(auto).values(), region, city, price_car_byn,
                                          price_car_usd, link, get_time_post(auto['publishedAt'])
                                          )

                            av_db.av_insert_table(all_params)
                        # иначе прекращаем цикл дальше искать нет смысла все объявления идут  котормые меньше времени
                        # которое указано в поиске
                        else:
                            break
                    page += 1
                    break
            except Exception as ex:
                print(ex)
        except Exception as ex:
            print(ex)
