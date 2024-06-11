from flask import Flask, request
import telebot
import logging

app = Flask(__name__)

TOKEN = "7277985551:AAF81u_-kZNBDfsQWrZI-uuSg-5dMMNaljg"  # Ваш токен
bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    logging.info("Index route accessed")
    return "Hello, this is the CapybaraCoin farming bot!"

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        logging.info(f"Received update: {update}")
        bot.process_new_updates([update])
        return '!', 200
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return 'Error', 500

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    try:
        webhook_url = f"https://capybaracoin.onrender.com/{TOKEN}"
        logging.info(f"Setting webhook to URL: {webhook_url}")
        s = bot.set_webhook(url=webhook_url)
        if s:
            logging.info("Webhook setup succeeded")
            return "Webhook setup ok"
        else:
            logging.error("Webhook setup failed")
            return "Webhook setup failed"
    except Exception as e:
        logging.error(f"Error setting webhook: {e}")
        return f"Error: {e}", 500

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        logging.info(f"Received /start command from user: {message.from_user.id}")
        bot.reply_to(message, "Welcome to the CapybaraCoin farming bot!")
    except Exception as e:
        logging.error(f"Error handling /start command: {e}")

if __name__ == '__main__':
    app.run(debug=True)