import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
import os

# بارگذاری توکن از فایل .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# راه اندازی ربات
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# لیست افراد و نقش‌ها
names = []  # لیست اسامی
roles = ["نقش 1", "نقش 2", "نقش 3", "نقش 4", "نقش 5"]  # نقش‌ها

# دستور شروع
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("سلام! خوش اومدی. برای دریافت نقش خودت پیام بده.")

# دستور برای ارسال نقش‌های تصادفی
@dp.message_handler(commands=['assign'])
async def assign_role(message: types.Message):
    if len(names) == 0:
        await message.reply("هیچ فردی برای تخصیص نقش ثبت نشده است.")
        return

    if len(roles) < len(names):
        await message.reply("نقش‌ها کافی نیستند! لطفاً نقش‌های بیشتری اضافه کنید.")
        return

    random.shuffle(roles)
    assigned_roles = dict(zip(names, roles))
    
    # ارسال نقش به هر شخص
    for name in names:
        await bot.send_message(name, f"سلام! نقش شما: {assigned_roles[name]}")

    await message.reply("نقش‌ها به افراد تخصیص داده شد!")

# ثبت افراد جدید برای تخصیص نقش
@dp.message_handler(commands=['add'])
async def add_name(message: types.Message):
    if message.from_user.username not in names:
        names.append(message.from_user.username)
        await message.reply(f"{message.from_user.username} به لیست افراد اضافه شد!")
    else:
        await message.reply(f"{message.from_user.username} قبلاً اضافه شده!")

# شروع ربات
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
