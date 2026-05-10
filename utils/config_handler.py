import configparser
import os

def get_api_key():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    
    if not os.path.exists(config_path):
        return None
    
    config.read(config_path)
    if 'API' in config and 'api_key' in config['API']:
        key = config['API']['api_key']
        if key and key != "OPENWEATHERMAP_ANAHTARINIZI_BURAYA_YAZIN":
            return key
    return None

def save_api_key(api_key):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    config['API'] = {'api_key': api_key}
    with open(config_path, 'w') as configfile:
        config.write(configfile)