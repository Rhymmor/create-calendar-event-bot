import logging
import httplib2
from apiclient import discovery
from parser import parse_message
from utils import get_env
from auth import check_auth, create_auth_url, create_credentials
from oauth2client.client import OAuth2Credentials
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
            if self.is_credentials_invalid(creds):
                logging.info('User {}: no credentials. Creating auth url'.format(user_id))
                url, flow = create_auth_url()
                logging.info(url)
 
                self.flows[user_id] = flow
                bot.send_message(chat_id=chat_id, text=url)
        
        return start

    def handle_code(self, bot, update):
        user_id = update.effective_user.id
        chat_id = update.message.chat_id
        logging.info('User {}: no credentials. Trying to apply code {}'.format(user_id, text))
        if create_credentials(user_id, self.flows[user_id], update.message.text):
            logging.info('User {}: Successfully authorized'.format(user_id))
            bot.send_message(chat_id=chat_id, text="Successfully authorized")
            self.flows.pop(user_id, None)
        else: 
            logging.info('User {}: Error while authorizing'.format(user_id))
            bot.send_message(chat_id=chat_id, text="Error while authorizing")

    def is_credentials_invalid(self, credentials):
        return not credentials or \
            not credentials['credentials'] or \
            OAuth2Credentials.from_json(credentials['credentials']).invalid

    def message_command(self):
        def parse_text(bot, update):
            user_id = update.effective_user.id
            text = update.message.text
            chat_id = update.message.chat_id

            creds = check_auth(user_id)
            if self.is_credentials_invalid(creds):
                self.handle_code(bot, update)
            else:
                credentials = OAuth2Credentials.from_json(creds['credentials'])
                http = credentials.authorize(httplib2.Http())
                service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)
                calendars = service.calendarList().list().execute()
                print(calendars)
                print()
                print()
                event = service.events().insert(calendarId='primary', body={
                    'summary': text, 
                    'end': {'date': '2017-10-04'},
                    'start': {'date': '2017-10-04'}
                }).execute()
                print(event)

                match = parse_message(text)
                if match is not None:
                    bot.send_message(chat_id=update.message.chat_id, text=match)
        
        return parse_text

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
