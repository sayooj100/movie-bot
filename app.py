from flask import Flask
import threading
import bot_main   # make sure bot_main.py has your bot = telebot.TeleBot(...)

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def run_bot():
    bot_main.bot.infinity_polling()

if __name__ == "__main__":
    # Start the bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()
    # Start Flask for Koyeb health check
    app.run(host="0.0.0.0", port=8080)











