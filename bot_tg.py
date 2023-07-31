from aiogram.utils import executor
from create_bot import dp
from sqlite_db import db_py


async def on_startup(_):
    # запуск функции базы данных
    print('Бот успешно запущен')
    db_py.db_start()

# импорт обработчиков
from handlers import client, params_url, other

#запуск обработчиков
client.register_handlers_client(dp)
params_url.register_handlers_params(dp)
other.register_handlers_other(dp)


# запсу бота
def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



if __name__ == '__main__':
    main()
