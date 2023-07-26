import datetime

def salute(time):
    lst_time = [datetime.time(i, 0, 0) for i in [4, 11, 17, 23]]
    greetings = ['Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи']
    return greetings[0] if lst_time[0] <= time < lst_time[1] else greetings[1] if lst_time[1] <= time < lst_time[2] else \
        greetings[2] if lst_time[2] <= time < lst_time[3] else greetings[3]


now_time = datetime.datetime.now().time()