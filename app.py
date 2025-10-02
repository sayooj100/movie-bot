from flask import Flask
import threading
import bot_main  # your bot code

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def run_bot():
    bot_main.infinity_polling()

# Start the bot in a separate thread
threading.Thread(target=run_bot, daemon=True).start()








