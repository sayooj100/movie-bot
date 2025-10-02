from flask import Flask
import threading
import bot_main  # your bot code lives here

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def run_bot():
    bot_main.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)





