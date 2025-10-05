import os
from flask import Flask, request
import telebot
from bot_main import bot

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN")
APP_URL = os.getenv("APP_URL")  # Example: https://your-app-name.koyeb.app

# Set webhook when app starts
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{API_TOKEN}")

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200






















