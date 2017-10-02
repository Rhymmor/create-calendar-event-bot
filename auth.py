
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from utils import get_env

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Create Calendar event Telegram Bot'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES, redirect_uri=get_env('REDIRECTION_URL'))
    flow.user_agent = APPLICATION_NAME
    if flags:
        authorize_url = flow.step1_get_authorize_url()
        print(authorize_url)
        code = input('Enter verification code: ').strip()
        credential = flow.step2_exchange(code)
        print(credential)
    return credentials

get_credentials()