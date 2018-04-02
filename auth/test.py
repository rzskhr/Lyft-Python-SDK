import json
import requests
from requests.auth import HTTPBasicAuth


PUBLIC_AUTH_URL = "https://api.lyft.com/oauth/token"


class LyftPublicAuth(object):
    def __init__(self, config, sandbox_mode=False):
        self.__sandbox_mode = sandbox_mode
        self.__config = config

    def get_access_token(self):
        header = {"content-type": "application/json"}

        client_id = self.__config['client_id']
        client_secret = self.__config['client_secret']

        data = {"grant_type": "client_credentials", "scope": "public"}

        response = requests.post(PUBLIC_AUTH_URL,
                                 headers=header,
                                 data=json.dumps(data),
                                 auth=HTTPBasicAuth(client_id, client_secret))

        #print(response.json())
        #print(response.headers)

        return {
            "headers": {
                "x-ratelimit-limit": response.headers.get('x-ratelimit-limit'),
                "x-ratelimit-remaining": response.headers.get('x-ratelimit-remaining'),
                "content-type": response.headers.get('content-type'),
                "cache-control": response.headers.get('cache-control'),
                "pragma": response.headers.get('pragma')
            },
            "token_type": response.json().get("token_type"),
            "access_token": response.json().get("access_token"),
            "expires_in": response.json().get("expires_in"),
            "scope": response.json().get("scope"),
        }









# get secret access keys
def get_secret_access():
    import configparser

    ACCESS_TOKEN_PATH = "/Users/Raj/Root/Code/_PRIVATE_KEYS/lyft/test_app.cfg"

    config = configparser.ConfigParser()
    config.read(ACCESS_TOKEN_PATH)

    client_id = config.get('lyft', 'client_id')
    client_secret = config.get('lyft', 'client_secret')

    return {"client_id": client_id, "client_secret": client_secret}


# create lyft_auth_object
lyft_auth_object = LyftPublicAuth(get_secret_access())

# access_token_obj
access_token_obj = lyft_auth_object.get_access_token()

headers = {"Authorization": "{} {}".format(
    access_token_obj.get('token_type'),
    access_token_obj.get('access_token'))
}

URL = "https://api.lyft.com/v1/eta?lat=37.7763&lng=-122.3918"

URL = "https://api.lyft.com/v1/ridetypes?lat=37.7763&lng=-122.3918"

response = requests.get(URL, headers=headers)

print(response.text)
