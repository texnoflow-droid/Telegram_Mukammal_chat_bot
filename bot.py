import telebot
import time
import logging
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ================== CONFIGURATION ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_CHANNEL_ID = int(os.getenv("SECRET_CHANNEL_ID", "-1001234567890"))

# List of target channels/groups for broadcasting
TARGET_CHATS_STR = os.getenv("TARGET_CHATS", "")
TARGET_CHATS = [int(x.strip()) for x in TARGET_CHATS_STR.split(",") if x.strip()]

if not BOT_TOKEN:
    raise ValueError("Please set BOT_TOKEN in .env file")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
logging.basicConfig(level=logging.INFO)

# ================== MEMORY ==================
USER_STATE = {}
MESSAGE_OWNER = {}

# ================== STEPS ==================
STEP_LANG = "choose_language"
STEP_CONTACT = "need_contact"
STEP_NAME = "wait_full_name"
STEP_READY = "registered"

# ================== HELPER FUNCTIONS ==================
def t(uid, uz, ru):
    lang = USER_STATE.get(uid, {}).get("lang", "uz")
    return ru if lang == "ru" else uz

def lang_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("🇺🇿 O'zbek tili", "🇷🇺 Русский язык")
    return kb

def contact_keyboard(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    text = "📋 Ro'yxatdan o'tish" if lang == "uz" else "📋 Зарегистрироваться"
    kb.add(KeyboardButton(text, request_contact=True))
    return kb

# ================== 🚀 ADMIN BROADCAST TO ALL ==================
# Forwards any new post from channel to all target chats
@bot.channel_post_handler(func=lambda m: m.chat.id == SECRET_CHANNEL_ID and not m.reply_to_message,
                          content_types=['text', 'photo', 'video', 'document', 'voice', 'audio', 'video_note', 'sticker', 'location'])
def auto_broadcast(message):
    logging.info(f"📢 New media/message received in channel. Starting broadcast...")
    
    success = 0
    for chat_id in TARGET_CHATS:
        try:
            bot.copy_message(chat_id, message.chat.id, message.message_id)
            success += 1
            time.sleep(0.3)  # Protection from Telegram limits
        except Exception as e:
            logging.error(f"Error in {chat_id}: {e}")
            
    bot.send_message(SECRET_CHANNEL_ID, f"📊 <b>Broadcast completed</b>\n✅ Successfully sent to {success} places.")

# ================== 📩 ADMIN REPLY (REPLY) ==================
@bot.channel_post_handler(func=lambda m: m.chat.id == SECRET_CHANNEL_ID and m.reply_to_message,
                          content_types=['text', 'photo', 'video', 'document', 'voice', 'audio', 'video_note', 'sticker'])
def admin_reply(message):
    rid = message.reply_to_message.message_id
    if rid not in MESSAGE_OWNER:
        return

    target_user_id = MESSAGE_OWNER[rid]
    try:
        bot.copy_message(target_user_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "✅ <b>Reply sent to user.</b>")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ <b>Error sending:</b> {e}")

# ================== 👤 USER PART (START) ==================
@bot.message_handler(commands=['start'])
def start(message):
    USER_STATE[message.from_user.id] = {"step": STEP_LANG}
    bot.send_message(
        message.chat.id,
        "👋 <b>Welcome!</b>\n\nPlease select your language:",
        reply_markup=lang_keyboard()
    )

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == STEP_LANG)
def choose_lang(message):
    uid = message.from_user.id
    if "🇺🇿" in message.text:
        USER_STATE[uid].update({"lang": "uz", "step": STEP_CONTACT})
        bot.send_message(message.chat.id, "✅ <b>O'zbek tili tanlandi</b>", reply_markup=contact_keyboard("uz"))
    elif "🇷🇺" in message.text:
        USER_STATE[uid].update({"lang": "ru", "step": STEP_CONTACT})
        bot.send_message(message.chat.id, "✅ <b>Русский язык выбран</b>", reply_markup=contact_keyboard("ru"))

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    uid = message.from_user.id
    USER_STATE[uid]["phone"] = message.contact.phone_number
    USER_STATE[uid]["step"] = STEP_NAME
    bot.send_message(message.chat.id, t(uid, "✍️ <b>Ism Familiyangizni kiriting:</b>", "✍️ <b>Введите ФИО:</b>"), reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == STEP_NAME)
def get_name(message):
    uid = message.from_user.id
    USER_STATE[uid]["full_name"] = message.text
    USER_STATE[uid]["step"] = STEP_READY
    
    # Notification to channel
    bot.send_message(SECRET_CHANNEL_ID, f"🆕 <b>New user:</b>\n👤 {message.text}\n📞 {USER_STATE[uid]['phone']}")
    
    bot.send_message(message.chat.id, t(uid, "✅ <b>Ready!</b> Now send your appeal.", "✅ <b>Готово!</b> Отправьте ваше обращение."))

# ================== 📨 RECEIVE APPEAL ==================
@bot.message_handler(func=lambda m: USER_STATE.get(m.from_user.id, {}).get("step") == STEP_READY,
                     content_types=['text', 'photo', 'video', 'document', 'voice', 'audio', 'video_note', 'sticker'])
def get_appeal(message):
    uid = message.from_user.id
    u = USER_STATE[uid]
    
    head = f"📩 <b>New appeal</b>\n👤 {u['full_name']}\n🆔 {uid}"
    bot.send_message(SECRET_CHANNEL_ID, head)
    
    # Copy any media type
    sent = bot.copy_message(SECRET_CHANNEL_ID, message.chat.id, message.message_id)
    MESSAGE_OWNER[sent.message_id] = uid
    
    bot.send_message(message.chat.id, t(uid, "🚀 <b>Sent!</b>", "🚀 <b>Отправлено!</b>"))

# ================== START ==================
if __name__ == "__main__":
    print("🤖 Bot running in universal mode...")
    bot.infinity_polling(skip_pending=True)
