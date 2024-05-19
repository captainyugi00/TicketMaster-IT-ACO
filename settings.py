import json

def get_config():

    config_data = None

    with open('config.json') as fp:
        config_data = json.load(fp)
        fp.close()

    return config_data
