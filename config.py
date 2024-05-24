from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from aiogram.client.session.aiohttp import AiohttpSession

PROXY_URL = 'http://proxy_server:3128'
session = AiohttpSession(proxy=PROXY_URL)
storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
ADMIN_ID=config('ADMIN_ID')
MEDIA_PATH = config('MEDIA_PATH')
bot = Bot(token=TOKEN, session=session)
db = Dispatcher()