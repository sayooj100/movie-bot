from flask import Flask
import threading
import bot_main  # rename your existing bot code file to bot_main.py

app = Flask(__name__)

# Health check endpoint
@app.route('/')
def health():
    return "OK", 200

# Run bot in a separate thread
def run_bot():
    bot_main.bot.infinity_polling()

if __name__ == '__main__':
    # Start bot thread
    threading.Thread(target=run_bot).start()
    # Start Flask app for health checks
    app.run(host='0.0.0.0', port=8080)
