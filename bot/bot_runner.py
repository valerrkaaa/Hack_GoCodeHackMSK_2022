from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_token import token
import aiogram

bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())

