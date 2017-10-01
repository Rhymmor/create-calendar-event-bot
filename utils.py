from os import environ

def get_env(name):
    if name not in environ:
        raise Exception("Environment variable '{}' is not set".format(name))
    return environ[name]
