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
    datetime = get_datetime_str(message)
    if datetime is None:
        return None, None
    title = message.replace(datetime, '')

    token = get_env('GOOGLE_API_TOKEN')
    entities, syntax = fetch(message, token)    #for now do nothing with results

    return datetime, title

def get_datetime_str(string):
    cal = pdt.Calendar()
    match = cal.nlp(string)
    if match is not None and len(match) > 0:
        return match[0][4]
    else:
        return None

def get_datetime(string):
    cal = pdt.Calendar()
    return cal.parse(string)

def get_location(res):
    entities_key = 'entities'
    if entities_key in res:
        locations = [entity for entity in res[entities_key] if entity['type'] is 'LOCATION']
        if len(locations > 0):
            return locations[0]

            