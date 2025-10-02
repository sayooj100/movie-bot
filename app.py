from flask import Flask
import threading
import bot_main  # Import your bot file (bot_main.py)

app = Flask(__name__)

# Health check endpoint for Koyeb
@app.route("/")
def health():
    return "OK", 200

# Start the bot in a separate thread
def start_bot():
    bot_main.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_bot, daemon=True).start()
    # Run Flask for health check
    app.run(host="0.0.0.0", port=8080)


