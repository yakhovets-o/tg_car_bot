import json
import aiohttp
import asyncio
import time
from datetime import datetime
import sqlite3 as sq


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'

}

base = sq.connect(r'C:\Users\lego\PycharmProjects\car_bot\search_option.db')
cur = base.cursor()
params = cur.execute('SELECT * FROM url').fetchall()
base.commit()
ready_list_cars = []


print('_____________________________________________________________________________________________________')

start = time.time()
async def get_url():
    count = 0
    client = 0
    start = time.time()
    for item in params:
        list_cars = []
        car, price_min, price_max, publ, user_id = item[0], item[1], item[2], item[3], item[4]
        client += 1
        print(f'клиент {client}')
        par = {'price_usd[min]': price_min, 'price_usd[max]': price_max,
               'creation_date': publ, 'sort': 4}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'https://api.av.by/offer-types/{car}/filters/main/init?', headers=HEADERS,
                                   params=par) as r:
                response = await r.json()
                big_url = r.url
                for page in range(int(response['pageCount'])):
                    async with session.get(url=big_url, headers=HEADERS, params={'page': page}) as url:
                        cars = await url.json()
                        for car in cars['adverts']:
                            count += 1
                            print(count)
                            print(car['publicUrl'])
                            list_cars.append(
                                {"car_name": f"{car['properties'][0]['value']} {car['properties'][1]['value']}",
                                 "car_url": car['publicUrl'],
                                 "param_car": f"{car['year']} год",
                                 "price_car_byn": f"{car['price']['byn']['amount']} Br",
                                 "price_car_usd": f"≈ {car['price']['usd']['amount']} Usd",
                                 "city_car": car['locationName'],
                                 "data_car": str(
                                     datetime.strptime(car['publishedAt'].replace('T', ' ').replace('+0000', ''),
                                                       '%Y-%m-%d %H:%M:%S'))
                                 }
                            )
            with open(rf'C:\Users\lego\PycharmProjects\car_bot\cars_users\{user_id}.json', mode='w', encoding='UTF-8') as file:
                json.dump(list_cars, file, ensure_ascii=False, indent=4)
    stop = time.time()
    print(stop - start)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
avto = asyncio.run(get_url())


# async def main():
#    loop = asyncio.new_event_loop()
#   asyncio.set_event_loop(loop)
#
#
# if __name__ == '__main__':
#
#     asyncio.run(main())

print('_____________________________________________________________________________________________________')
# with open(r'C:\Users\lego\PycharmProjects\car_bot\cars_users\504152070.json', encoding='utf-8') as file:
#     a = json.load(file)
# for i in a:
#     print(i['car_name'])
#     print(i['car_url'])
