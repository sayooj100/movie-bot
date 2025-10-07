import os
import telebot
from flask import Flask, request
import bot_main

API_TOKEN = os.getenv("API_TOKEN")

bot = bot_main.bot
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is Running on Render!"

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == "__main__":
    # Webhook setup
    port = int(os.environ.get("PORT", 8080))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-render-app-name.onrender.com/{API_TOKEN}")
    app.run(host="0.0.0.0", port=port)


























