from oauth2client import client
from oauth2client import tools
from oauth2client import OAuth2Credentials
from utils import get_env
from database import Database
    
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Create Calendar event Telegram Bot'

def create_credentials():
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES, redirect_uri=get_env('REDIRECTION_URL'))
    flow.user_agent = APPLICATION_NAME
    authorize_url = flow.step1_get_authorize_url()
    print(authorize_url)
    code = input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    return credentials

def check_auth(user_id):
    db = Database()
    creds = db.get_credentials(user_id)

def get_credentials(user_id):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    db = Database()
    creds = db.get_credentials(user_id)
    if creds:
        return OAuth2Credentials.from_json(creds['credentials'])
    else:
        new_creds = create_credentials()
        db.insert_credentials(user_id, new_creds)
        return new_creds