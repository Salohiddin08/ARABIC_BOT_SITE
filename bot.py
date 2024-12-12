import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from datetime import datetime, timedelta
import os
import django
from django.core.exceptions import ObjectDoesNotExist
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  
django.setup()

from project.models import User  

BOT_TOKEN = "7202425137:AAHNadLXM93o9XWyX_wGejPqOpnpI5jCaUk"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@sync_to_async
def set_verification_code(phone_number, verification_code, expiry_time):
    try:
        user = User.objects.get(phone_number=phone_number)
        user.verification_code = verification_code
        user.code_expiration = expiry_time
        user.save()
        logger.info(f"Verification code set for user {user.username}")
    except ObjectDoesNotExist:
        logger.error("User not found")

@sync_to_async
def verify_user_code(verification_code):
    try:
        user = User.objects.get(verification_code=verification_code)
        return user
    except ObjectDoesNotExist:
        return None

@dp.message(Command(commands=["start"]))
async def handle_start(message: types.Message):
    await message.reply(
        "Salom! Telefon raqamingizni yuboring, masalan: <code>+998901234567</code>"
    )

@dp.message(lambda message: message.text.startswith("+"))
async def handle_phone_number(message: types.Message):
    phone_number = message.text.strip()
    verification_code = str(datetime.now().microsecond)[:6]
    expiry_time = datetime.now() + timedelta(minutes=1)

    await set_verification_code(phone_number, verification_code, expiry_time)

    await message.reply(
        f"Raqamingiz qabul qilindi: {phone_number}\nTasdiqlash kodi: <code>{verification_code}</code>\nIltimos, kodni kiriting."
    )

@dp.message(lambda message: message.text.isdigit() and len(message.text) == 6)
async def handle_verification_code(message: types.Message):
    verification_code = message.text.strip()
    user = await verify_user_code(verification_code)

    if user:
        if user.code_expiration > datetime.now():
            user.is_verified = True
            await sync_to_async(user.save)()
            await message.reply("Tasdiqlash muvaffaqiyatli yakunlandi! Siz ro'yxatdan o'tdingiz!")
        else:
            await message.reply("Tasdiqlash kodi muddati o'tgan. Yangi kod so'rang.")
    else:
        await message.reply("Tasdiqlash kodi noto'g'ri.")

async def main():
    logger.info("Bot started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
