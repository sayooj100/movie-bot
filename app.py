from flask import Flask, request
import telebot
import os

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://<your-koyeb-domain>/webhook

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ---------------- Include your existing handlers here ----------------
# Copy all the handlers (start, admin flow, user flow) from your bot code above

# ---------------- Webhook route ----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    if json_data:
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
    return "OK", 200

# ---------------- Health check ----------------
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

# ---------------- Set webhook on startup ----------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Bot is running! Webhook set to: {WEBHOOK_URL}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

