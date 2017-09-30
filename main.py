import os
import logging
from telegram.ext import Updater, CommandHandler

def set_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, human!")


def main():
    set_logging()
    token_env = 'BOT_TOKEN'
    if token_env not in os.environ:
        raise Exception("Environment variable '{}' is not set".format(token_env))
    bot_token = os.environ['BOT_TOKEN']
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher 
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

main()
