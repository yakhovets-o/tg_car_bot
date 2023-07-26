import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage = MemoryStorage()
admin = os.getenv('ADMIN')
support = os.getenv('SUPPORT')
bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(bot, storage=storage)