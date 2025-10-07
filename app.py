import os
import threading
import time
from flask import Flask
import bot_main  # Import your Telegram bot file here

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on Render!"

def run_bot():
    bot_main.run_bot()  # Function inside bot_main.py that starts polling

if __name__ == "__main__":
    # Run the bot in a background thread
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
























