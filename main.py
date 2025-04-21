import asyncio
import os
import json
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Установи переменную окружения.")

# Загрузка базы чаёв
with open("tea_db.json", encoding="utf-8") as f:
    tea_db = json.load(f)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я T-Effect Bot. Напиши /list, чтобы увидеть все чаи, или /tea <название>, чтобы получить подробную карточку."
    )

# Команда /list
@dp.message(F.text == "/list")
async def list_handler(message: types.Message):
    names = [f"• {name.title()}" for name in tea_db.keys()]
    await message.answer("📋 Чаи в базе:\n\n" + "\n".join(names))

# Команда /tea <название>
@dp.message(F.text.startswith("/tea"))
async def tea_handler(message: types.Message):
    name = message.text.replace("/tea", "").strip().lower()
    tea = tea_db.get(name)
    if not tea:
        await message.answer("⚠️ Чай не найден. Попробуй /list.")
        return

    text = f"<b>{name.title()}</b>\n\n"
    for key, val in tea.items():
        text += f"<b>{key}:</b> {val}\n"
    await message.answer(text)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
