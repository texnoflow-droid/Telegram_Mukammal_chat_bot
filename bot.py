import asyncio
import logging
import re
import os
from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1003694678917"))

if not GROQ_API_KEY or not TELEGRAM_TOKEN:
    raise ValueError("Please set GROQ_API_KEY and TELEGRAM_TOKEN in .env file")

client = Groq(api_key=GROQ_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


# --- 1. ADMIN REPLY TO USER (REPLY SYSTEM) ---
@dp.message(F.chat.id == LOG_GROUP_ID, F.reply_to_message)
async def admin_reply_handler(message: types.Message):
    # Get the text of the replied message (bot's message)
    source_text = message.reply_to_message.text or message.reply_to_message.caption
    
    if not source_text:
        return

    try:
        # Search for "ID: 1234567" pattern in the text
        # This line is very important!
        match = re.search(r"ID:\s?(\[?\d+\]?)", source_text)
        
        if match:
            # Keep only digits
            user_id = int(re.sub(r"\D", "", match.group(1)))
            
            # Send admin's message to the user
            if message.text:
                await bot.send_message(user_id, f"<b>Admin javobi:</b>\n\n{message.text}", parse_mode="HTML")
                await message.reply(f"✅ Xabar yuborildi! (ID: {user_id})")
            else:
                await message.reply("⚠️ Faqat matnli javob yubora olasiz.")
        else:
            await message.reply("❌ Xatodan ID raqami topilmadi. Bot yuborgan xabarga reply qiling!")
            
    except Exception as e:
        logging.error(f"Reply xatosi: {e}")
        await message.reply(f"❌ Yuborishda xatolik: {e}")


# --- 2. START AND REGISTRATION ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Ro'yxatdan o'tish", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer(f"Salom {message.from_user.full_name}! Botdan foydalanish uchun ro'yxatdan o'ting.", reply_markup=kb)


@dp.message(F.contact)
async def contact_handler(message: types.Message):
    user = message.from_user
    contact = message.contact
    
    await message.answer("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi savol yuborishingiz mumkin.", reply_markup=types.ReplyKeyboardRemove())
    
    # Full report to admin
    admin_msg = (
        f"🌟 <b>Yangi foydalanuvchi ro'yxatdan o'tdi!</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Ism: {html.quote(user.full_name)}\n"
        f"📞 Tel: +{contact.phone_number}\n"
        f"🔗 Username: @{user.username if user.username else 'yoq'}\n"
        f"🆔 ID: {user.id}\n"
        f"━━━━━━━━━━━━━━"
    )
    await bot.send_message(LOG_GROUP_ID, admin_msg, parse_mode="HTML")


# --- 3. CHAT AND GROQ AI ---
@dp.message(F.chat.type == "private")
async def chat_handler(message: types.Message):
    if not message.text:
        return

    # Effects
    try:
        await message.react(reactions=[ReactionTypeEmoji(emoji="👀")])
    except:
        pass
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        # Get response from Groq
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}]
        )
        bot_res = completion.choices[0].message.content

        # Beautiful formatted report to admin
        user = message.from_user
        log_report = (
            f"📥 <b>Foydalanuvchi xabari:</b>\n"
            f"«{html.quote(message.text)}»\n\n"
            f"🤖 <b>Bot javobi:</b>\n"
            f"«{html.quote(bot_res[:800])}...»\n\n"
            f"👤 <b>Mijoz:</b> {html.quote(user.full_name)}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else 'yoq'}\n"
            f"🆔 ID: {user.id}"  # <--- This line is REQUIRED for REPLY to work!
        )
        
        await bot.send_message(LOG_GROUP_ID, log_report, parse_mode="HTML")
        await message.answer(bot_res)
        await message.react(reactions=[])

    except Exception as e:
        await message.answer("Xatolik yuz berdi. 😵💫")
        await bot.send_message(LOG_GROUP_ID, f"❌ Xatolik: {e}\nID: {message.from_user.id}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
