import telebot
from telebot import types
import random
import string
import os
from pymongo import MongoClient

# ---------------- Environment Variables ----------------
API_TOKEN = os.getenv("API_TOKEN")              # Telegram bot token
MONGO_URI = os.getenv("MONGO_URI")              # MongoDB connection string
ADMIN_ID = int(os.getenv("ADMIN_ID"))
STORAGE_GROUP_ID = int(os.getenv("STORAGE_GROUP_ID"))
FIXED_CHANNEL_1 = os.getenv("FIXED_CHANNEL_1")  # Public channel

# ---------------- MongoDB Connection ----------------
try:
    client = MongoClient(MONGO_URI, tls=True)
    db = client["telegram_bot"]
    channels_col = db["private_channels"]
    batches_col = db["batches"]
   # print("MongoDB connected")
except Exception as e:
   # print("MongoDB connection failed:", e)
    channels_col = None
    batches_col = None

# ---------------- Initialize Bot ----------------
bot = telebot.TeleBot(API_TOKEN, threaded=True)  # threaded=True ensures safe concurrent polling

# ---------------- In-Memory Data ----------------
private_channels = {}  # {admin_id: {"chat_id": int, "invite_link": str}}
files_db = {}          # {random_code: {"files": [...], "admin_id": id}}
pending_batches = {}   # {admin_id: {"code": str, "files": [...], "invite_link": str, "chat_id": int}}

# ---------------- Command Handlers ----------------
@bot.message_handler(commands=['start'])
def start_command(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Send the invite link of your private channel.")
        bot.register_next_step_handler(message, ask_private_channel_link)
    else:
        args = message.text.split()
        if len(args) > 1:
            code = args[1]
            handle_user_request(message, code)
        else:
            bot.send_message(message.chat.id, "Hello! Use a valid link to access files.")

# ---------------- Admin Flow ----------------
def ask_private_channel_link(message):
    admin_id = message.chat.id
    pending_batches[admin_id] = {"invite_link": message.text.strip()}
    bot.send_message(admin_id, "Send the numeric chat ID of this private channel:")
    bot.register_next_step_handler(message, save_private_channel_id)

def save_private_channel_id(message):
    admin_id = message.chat.id
    try:
        chat_id = int(message.text.strip())
        invite_link = pending_batches[admin_id]["invite_link"]

        # Save in MongoDB
        if channels_col:
            channels_col.update_one(
                {"admin_id": admin_id},
                {"$set": {"chat_id": chat_id, "invite_link": invite_link}},
                upsert=True
            )

        private_channels[admin_id] = {"chat_id": chat_id, "invite_link": invite_link}

        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        pending_batches[admin_id].update({"code": code, "files": [], "chat_id": chat_id})

        bot.send_message(admin_id,
            f"✅ Private channel saved!\nSend files now. Type /done when finished."
        )
    except ValueError:
        bot.send_message(admin_id, "❌ Invalid chat ID. Please send a numeric chat ID.")

@bot.message_handler(content_types=["document", "video", "photo"])
def collect_files(message):
    admin_id = message.chat.id
    if admin_id in pending_batches:
        forwarded = bot.forward_message(STORAGE_GROUP_ID, admin_id, message.message_id)
        pending_batches[admin_id]["files"].append(forwarded.message_id)
        bot.send_message(admin_id,
            f"✅ File added ({len(pending_batches[admin_id]['files'])} total)"
        )

@bot.message_handler(commands=['done'])
def finalize_batch(message):
    admin_id = message.chat.id
    if admin_id in pending_batches and pending_batches[admin_id]["files"]:
        batch = pending_batches[admin_id]

        # Save in MongoDB
        if batches_col:
            batches_col.insert_one({
                "code": batch["code"],
                "admin_id": admin_id,
                "files": batch["files"]
            })

        files_db[batch["code"]] = {"files": batch["files"], "admin_id": admin_id}
        del pending_batches[admin_id]

        bot.send_message(admin_id,
            f"✅ Files saved!\nLink:\nhttps://t.me/{bot.get_me().username}?start={batch['code']}"
        )
    else:
        bot.send_message(admin_id, "❌ No files added. Send files first.")

# ---------------- User Flow ----------------
def handle_user_request(message, code):
    user_id = message.chat.id

    # Try memory first
    batch = files_db.get(code)

    # Try MongoDB if not in memory
    if not batch and batches_col:
        db_batch = batches_col.find_one({"code": code})
        if db_batch:
            batch = {"files": db_batch["files"], "admin_id": db_batch["admin_id"]}
            files_db[code] = batch
        else:
            bot.send_message(user_id, "❌ Invalid or expired link.")
            return

    admin_id = batch["admin_id"]
    ch2 = private_channels.get(admin_id)
    if not ch2 and channels_col:
        db_ch = channels_col.find_one({"admin_id": admin_id})
        if db_ch:
            ch2 = {"chat_id": db_ch["chat_id"], "invite_link": db_ch["invite_link"]}
            private_channels[admin_id] = ch2
        else:
            bot.send_message(user_id, "❌ Channel info not found.")
            return

    try:
        m1 = bot.get_chat_member(FIXED_CHANNEL_1, user_id)
        m2 = bot.get_chat_member(ch2["chat_id"], user_id)

        if m1.status in ["member", "administrator", "creator"] and \
           m2.status in ["member", "administrator", "creator"]:
            for msg_id in batch["files"]:
                bot.copy_message(user_id, STORAGE_GROUP_ID, msg_id)
        else:
            ask_to_join(user_id, FIXED_CHANNEL_1, ch2["invite_link"], code)
    except:
        ask_to_join(user_id, FIXED_CHANNEL_1, ch2["invite_link"], code)

def ask_to_join(user_id, ch1, invite_link, code):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("✅ Join Channel 1", url=f"https://t.me/{ch1.strip('@')}")
    btn2 = types.InlineKeyboardButton("✅ Join Channel 2", url=invite_link)
    retry_btn = types.InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{bot.get_me().username}?start={code}")
    markup.add(btn1, btn2, retry_btn)
    bot.send_message(user_id, "⚠️ Join both channels to access files.", reply_markup=markup)

# ---------------- RUN BOT ----------------














