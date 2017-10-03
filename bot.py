import logging
import httplib2
from apiclient import discovery
from parser import parse_message, get_datetime
from utils import get_env, get_rfc3339_time
from auth import check_auth, create_auth_url, create_credentials
from oauth2client.client import OAuth2Credentials
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

class Bot:
    def __init__(self):
        bot_token = get_env('BOT_TOKEN')
        self.updater = Updater(token=bot_token)
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.__start_command())
        message_handler = MessageHandler(Filters.text, self.__message_command())

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(message_handler)

        self.flows = {}

    def __start_command(self):
        def start(bot, update):
            chat_id = update.message.chat_id
            bot.send_message(chat_id=chat_id, text="Hello, human!")

            user_id = update.effective_user.id
            creds = check_auth(user_id)
            if self.__is_credentials_invalid(creds):
                logging.info('User {}: no credentials. Creating auth url'.format(user_id))
                url, flow = create_auth_url()
                logging.info(url)
 
                self.flows[user_id] = flow
                bot.send_message(chat_id=chat_id, text=url)
        
        return start

    def __handle_code(self, bot, update):
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

    def __get_oath2_credentials(self, credentials):
        return OAuth2Credentials.from_json(credentials['credentials'])

    def __is_credentials_invalid(self, credentials):
        return not credentials or \
            not credentials['credentials'] or \
            OAuth2Credentials.from_json(credentials['credentials']).invalid

    def __build_google_api_service(self, credentials):
        oath2_credentials = self.__get_oath2_credentials(credentials)
        http = oath2_credentials.authorize(httplib2.Http())
        return discovery.build('calendar', 'v3', http=http, cache_discovery=False)

    def __handle_event_message(self, bot, update, credentials):
        text = update.message.text
        chat_id = update.message.chat_id
        time_match, title = parse_message(text)
        if time_match is None:
            bot.send_message(chat_id=chat_id, text='Please, specify event time')
            raise Exception('There is no datetime in the message: {}'.format(text))

        service = self.__build_google_api_service(credentials)
        time_struct = get_datetime(time_match)
        event = service.events().insert(calendarId='primary', body={
            'summary': title,
            'end': {'dateTime': get_rfc3339_time(time_struct[0])},
            'start': {'dateTime': get_rfc3339_time(time_struct[0])}
        }).execute()
        bot.send_message(chat_id=chat_id, text='Created event with title: "{}" and time "{}"'.format(title, time_match))
        logging.info(event)

    def __message_command(self):
        def parse_text(bot, update):
            user_id = update.effective_user.id
            text = update.message.text
            chat_id = update.message.chat_id

            creds = check_auth(user_id)
            if self.__is_credentials_invalid(creds):
                self.__handle_code(bot, update)
            else:
                self.__handle_event_message(bot, update, creds)
        
        return parse_text

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
