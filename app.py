# app.py
from flask import Flask
import threading
import bot_main  # your bot code lives here

app = Flask(__name__)

# Health check endpoint
@app.route("/")
def health():
    return "OK", 200

# Function to run your Telegram bot
def run_bot():
    bot_main.infinity_polling()

# Start the bot in a background thread when the app loads
threading.Thread(target=run_bot, daemon=True).start()







