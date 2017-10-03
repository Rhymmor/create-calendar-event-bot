from parser import parse_message
from utils import get_env
from auth import check_auth, create_auth_url, create_credentials
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

class Bot:
    def __init__(self):
        bot_token = get_env('BOT_TOKEN')
        self.updater = Updater(token=bot_token)
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start_command())
        message_handler = MessageHandler(Filters.text, self.message_command())

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(message_handler)

        self.flows = {}

    def start_command(self):
        def start(bot, update):
            chat_id = update.message.chat_id
            bot.send_message(chat_id=chat_id, text="Hello, human!")

            user_id = update.effective_user.id
            creds = check_auth(user_id)
            if not creds or not creds['credentials']:
                url, flow = create_auth_url()
                self.flows[user_id] = flow
                bot.send_message(chat_id=chat_id, text=url)
        
        return start

    def message_command(self):
        def parse_text(bot, update):
            user_id = update.effective_user.id
            text = update.message.text
            chat_id = update.message.chat_id

            creds = check_auth(user_id)
            if not creds or not creds['credentials']:
                if create_credentials(user_id, self.flows[user_id], text):
                    bot.send_message(chat_id=chat_id, text="Successfully authorized")
                    self.flows.pop(user_id, None)
                else: 
                    bot.send_message(chat_id=chat_id, text="Error while authorizing")
            else:
                match = parse_message(text)
                if match is not None:
                    bot.send_message(chat_id=update.message.chat_id, text=match)
        
        return parse_text

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
