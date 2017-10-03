from os import environ
from time import mktime
from datetime import datetime

def get_env(name):
    if name not in environ:
        raise Exception("Environment variable '{}' is not set".format(name))
    return environ[name]

def get_rfc3339_time(struct_time):
    return datetime.fromtimestamp(mktime(struct_time)).isoformat('T') + 'Z'

