from flask import Flask
import threading
import bot_main  # imports your bot logic

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def run_bot():
    print("Bot thread starting...")
    bot_main.bot.infinity_polling()

if __name__ == "__main__":
    # Start the bot in a separate thread
    threading.Thread(target=run_bot, daemon=True).start()
    # Start Flask for health checks
    app.run(host="0.0.0.0", port=8080)




















