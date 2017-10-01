import socket
import requests as req
import parsedatetime as pdt
from utils import get_env
import json

def get_post_payload(message):
    return json.dumps({
        "encodingType": "UTF8",
        "document": {
            "type": "PLAIN_TEXT",
            "content": message
        }
    })

def post_googleapi(url, message):
    return req.post(url, data=get_post_payload(message))


def fetch_syntax(message, token):
    url = 'https://language.googleapis.com/v1/documents:analyzeSyntax?key={}'.format(token)
    return post_googleapi(url, message)

def fetch_entities(message, token):
    url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key={}'.format(token)
    return post_googleapi(url, message)

def fetch(message, token):
    entities = fetch_entities(message, token)
    syntax = fetch_syntax(message, token)
    return entities, syntax

def parse_message(message):
    datetime = get_datetime(message)
    if datetime is None:
        raise Exception('There is no datetime in the message: {}'.format(message))
    title = message.replace(datetime, '')

    token = get_env('GOOGLE_API_TOKEN')
    entities, syntax = fetch(message, token)    #for now do nothing with results

    return datetime

def get_datetime(string):
    cal = pdt.Calendar()
    match = cal.nlp(string)
    if match is not None and len(match) > 0:
        return match[0][4]
    else:
        return None