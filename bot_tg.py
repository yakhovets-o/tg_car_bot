from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print('Бот успешно запущен')


from handlers import client, params_url, other

client.register_handlers_client(dp)
params_url.register_handlers_params(dp)
other.register_handlers_other(dp)



def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
