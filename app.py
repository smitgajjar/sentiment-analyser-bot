from flask import Flask, request, jsonify

from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL

app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)

@app.route('/webhook', methods=['POST', 'GET'])
def index():
    req = request.get_json()
    bot = TelegramBot()
    bot.parse_webhook_data(req)
    success = bot.action()
    return jsonify(success=success)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    