from flask import Flask
import threading
import bot_main  # your bot code lives here

app = Flask(__name__)

# --- Health check endpoint ---
@app.route("/")
def health():
    return "OK", 200

# --- Start bot in a daemon thread ---
def start_bot():
    print("Bot is starting...")
    bot_main.infinity_polling()

if __name__ == "__main__":
    # Start the bot in background
    threading.Thread(target=start_bot, daemon=True).start()
    
    # Run Flask to handle Koyeb health checks
    app.run(host="0.0.0.0", port=8080)

















