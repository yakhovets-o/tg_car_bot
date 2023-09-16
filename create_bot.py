import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage = MemoryStorage()
admin = os.getenv('ADMIN')
support = os.getenv('SUPPORT')
bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)

vk_token = os.getenv('VK_TOKEN')
vk_version_api = os.getenv('VK_VERSION_API')
vk_url = os.getenv('VK_URL')
vk_count = os.getenv('VK_COUNT')
vk_groups = os.getenv('VK_GROUPS')


db_host = os.getenv('MY_DB_HOST')
db_port = os.getenv('MY_DB_PORT')
db_user = os.getenv('MY_DB_USER')
db_password = os.getenv('MY_DB_PASSWORD')
db_database = os.getenv('MY_DB_DATABASE')


dp = Dispatcher(bot, storage=storage)


# импорты