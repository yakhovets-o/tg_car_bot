import logging
from aiogram.utils import executor
from create_bot import dp
from handlers import client, params_url, other, parser
from mysql_db.connect_to_db import check_connect



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    # запуск функции базы данных
    print('Бот успешно запущен')
    check_connect()


# запуск обработчиков
client.register_handlers_client(dp)
params_url.register_handlers_params(dp)
parser.register_handlers_kuf_pars(dp)
other.register_handlers_other(dp)


# запсуск бота
def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
