from oauth2client import client
from utils import get_env
from database import Database
    
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Create Calendar event Telegram Bot'

def create_auth_url():
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES, redirect_uri=get_env('REDIRECTION_URL'), prompt='consent')
    flow.user_agent = APPLICATION_NAME
    authorize_url = flow.step1_get_authorize_url()
    return authorize_url, flow

def exchange_auth_code(flow, code):
    try:
        return flow.step2_exchange(code)
    except FlowExchangeError:
        return None

def create_credentials(user_id, flow, code):
    credentials = exchange_auth_code(flow, code)
    if credentials:
        db = Database()
        db.insert_credentials(user_id, credentials)
        return True
    return False

def check_auth(user_id):
    db = Database()
    return db.get_credentials(user_id)

