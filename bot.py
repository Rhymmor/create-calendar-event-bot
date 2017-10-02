from parser import parse_message
from utils import get_env
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, human!")

def parse_time(bot, update):
    match = parse_message(update.message.text)
    if match is not None:
        bot.send_message(chat_id=update.message.chat_id, text=match)

def start_bot():
    bot_token = get_env('BOT_TOKEN')
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text, parse_time)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()
