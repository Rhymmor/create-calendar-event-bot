import os
import logging
import parsedatetime as pdt
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

def set_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, human!")

def get_date(string):
    cal = pdt.Calendar()
    match = cal.nlp(string)
    if match is not None and len(match) > 0:
        return match[0][4]
    else:
        return None

def parse_time(bot, update):
    match = get_date(update.message.text)
    if match is not None:
        bot.send_message(chat_id=update.message.chat_id, text=match)

def main():
    set_logging()
    token_env = 'BOT_TOKEN'
    if token_env not in os.environ:
        raise Exception("Environment variable '{}' is not set".format(token_env))
    bot_token = os.environ['BOT_TOKEN']
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
