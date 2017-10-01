import os
import logging
from parser import parse_message
from utils import get_env
import parsedatetime as pdt
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.ext.dispatcher import run_async

def set_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, human!")

def parse_time(bot, update):
    match = parse_message(update.message.text)
    if match is not None:
        bot.send_message(chat_id=update.message.chat_id, text=match)

def main():
    set_logging()
    bot_token = get_env('BOT_TOKEN')
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text, parse_time)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

try:
    main()
except KeyboardInterrupt:
    exit()
