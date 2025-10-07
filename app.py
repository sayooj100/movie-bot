import os
import threading
from flask import Flask
import bot_main  # your main bot file

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is running!"

def run_bot():
    # Start the bot’s polling in a background thread
    bot_main.bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    # Run bot in a separate thread
    threading.Thread(target=run_bot).start()

    # Start Flask server (required for Koyeb/Render health checks)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)




























