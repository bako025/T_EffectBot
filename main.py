import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# === Загрузка переменных окружения ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Установи переменную окружения.")

# === Инициализация бота и диспетчера ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# === /start ===
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я T-Effect Bot. Подбираю китайский чай по эффекту, вкусу и настроению.\n\n"
        "Напиши что-то вроде:\n<i>хочу расслабиться</i>\nили нажми /list для просмотра всех чаёв."
    )

# === /list ===
@dp.message(F.text == "/list")
async def list_handler(message: types.Message):
    teas = ["Да Хун Пао", "Шу Пуэр (7581)", "Лун Цзин"]
    await message.answer("📋 Вот список чаёв:\n\n" + "\n".join(f"• {t}" for t in teas))

# === /tea <название> ===
@dp.message(F.text.startswith("/tea"))
async def tea_handler(message: types.Message):
    name = message.text.replace("/tea", "").strip().lower()
    if name == "да хун пао":
        await message.answer("<b>Да Хун Пао</b>\nТип: Улун\nРегион: Уишань\nЭффект: расслабляет, фокусирует\nЗаварка: проливами 95-100°C или в термосе.")
    else:
        await message.answer("⚠️ Чай не найден. Попробуй /list или /tea Да Хун Пао.")

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())