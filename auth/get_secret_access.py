import configparser

ACCESS_TOKEN_PATH = "/Users/Raj/Root/Code/_PRIVATE_KEYS/lyft/test_app.cfg"

config = configparser.ConfigParser()
config.read(ACCESS_TOKEN_PATH)

client_id = config.get('lyft', 'client_id')
client_secret = config.get('lyft', 'client_secret')

