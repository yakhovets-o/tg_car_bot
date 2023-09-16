import re
import json
import time
import requests
from string import punctuation
from datetime import datetime
from mysql_db import vk_db
from create_bot import vk_token, vk_url, vk_count, vk_version_api, vk_groups

# регулярки для форматирования данных из json
seller_id = re.compile(r'(?<=\[)id\d+(?=|)')
seller_price = re.compile(r'\d{,2}.?\d+(?= ?\$| ?у\.?е| ?y\.?e)')
seller_text = re.compile(r'(\[id.+\])|(📩.+\n.\n.+)')


# # функция для получения json  из групп
def get_json(user_id):
    for group in vk_groups.split(','):
        domain = group
        # формирование url запроса
        try:
            url_group = requests.get(url=vk_url, params={
                'domain': domain,
                'count': vk_count,
                'access_token': vk_token,
                'v': vk_version_api
            })
            # засыпаем ибо api не дает делать больше 3 запросов в сек
            time.sleep(3)
            # записываем json в json файл
            with open(fr'parsers/vk.ads/{user_id}_{group}.json', mode='w', encoding='utf-8') as file:
                json.dump(url_group.json(), file, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)


# фун-ция для получения url поста
def link_post(group, post_from_id, post_id):
    return rf"https://vk.com/{group}?w=wall{post_from_id}_{post_id}"


# фун-ция получения времени и сравнении его с временем, которое указал пользователь
# если время меньше чем указал пользователь этот пост не учитывается
# из json поступает unix время его нужно перевести с учетом  пояса времени
def get_time(unix_time):
    unix_timestamp = int(unix_time)
    timee = datetime.fromtimestamp(unix_timestamp)
    user_time = datetime.strptime(timee.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    return user_time


# фун-ция получения суммы  и сравнении его с суммой , которую  указал пользователь
# если сумма больше  чем указал пользователь этот пост не учитывается
# если сумму в посте  регулярка не нашла сумма становиться ровна 0
def get_price(text_post):
    user_price = seller_price.findall(text_post)
    price = 0 if not user_price else int(float(str(user_price[0]).strip(punctuation).replace(' ', '')
                                               .encode('ascii', 'ignore')))
    return price


# фун-ция  для получения ссылки
def get_link(post, group, text):
    # если группа  auto_moto_minsk
    if group == 'auto_moto_minsk':
        user_id = seller_id.findall(text)
        link = rf"https://vk.com/id{post['signer_id']}" if 'signer_id' in post \
            else rf"https://vk.com/{str(*user_id)}"

        return link

    # # если группа  не auto_moto_minsk,  если  ключ 'copyright'(ссылка на пост  Извне) нет
    if 'copyright' not in post and group != 'auto_moto_minsk':
        link = rf"https://vk.com/id{post['signer_id']}"
        return link

    # # если группа  не auto_moto_minsk, если  ключа 'copyright' (ссылка на пост  Извне) есть
    if 'copyright' in post and group != 'auto_moto_minsk':
        link = post['copyright']['link']
        return link


# фун-ции get_link, get_bool_price, get_bool_time, link_post являются вспологательныи и используются внутри
# функция для парсинга  данных из групп
def get_post(user_id, tracing_data, price_max):
    for group in vk_groups.split(','):
        # открываем файл с данными из группы
        with open(fr'parsers/vk.ads/{user_id}_{group}.json', mode='r', encoding='utf-8') as file:
            group_posts = json.load(file)

            # проходим посты группы в цикле
            for post in group_posts['response']['items']:
                text = post['text']
                body = seller_text.split(text)[0]

                # обернул в try except ибо есть посты которые не содержат необходимой нам ифны(реклама)
                # то формируем необходимые переменные и записываем их в дб(или другое место хранения)
                try:
                    # если время поста больше чем указал пользователь и если сумма в посте меньше чем указал пользователь
                    # и если ключа  'is_pinned' (закрепленный пост) нет
                    # и если ключа 'copy_history' (репост в паблик) нет
                    # если объявления нет в таблице в которой хранятся объявления которые уже были отправлены пользователю
                    if 'is_pinned' not in post and get_time(post['date']) > tracing_data and \
                            get_price(body) < price_max and 'copy_history' not in post:
                        all_params = (
                            user_id, link_post(group, post['from_id'], post['id']), get_link(post, group, text), body,
                            get_time(post['date']),
                        )

                        vk_db.vk_insert_table(all_params)
                except KeyError:
                    continue
