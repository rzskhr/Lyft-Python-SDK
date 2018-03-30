import json
import requests
from requests.auth import HTTPBasicAuth

AUTH_URL    = "https://api.lyft.com/oauth/token"


class LyftPublicAuth:
    """Authentication class for the 2 legged flow. This calls does not need user data and can access the public
    endpoints directly with the client secret and client ID. After successful authentication it will retrurn the
    access token

    """
    __sandbox_mode = None
    __config       = None

    def __init__(self, config, sandbox_mode=False):
        """

        :param sandbox_mode: Set to True if you want a sandbox environment else False
        :param config: Dictionary of client_id and client_secret

        """
        # TODO add exception here for config
        self.__sandbox_mode = sandbox_mode
        self.__config       = config

    def get_access_token(self):
        """Retrieves the access token along with the expiration time and rate limiting data in a dictionary

        :return: authentication_object
        :rtype: dict
        """
        header = {"content-type": "application/json"}

        # TODO add exception here for config
        client_id       = self.__config.get("client_id")
        if self.__sandbox_mode is False:
            client_secret   = self.__config.get("client_secret")
        else:
            client_secret   = "SANDBOX-{}".format(self.__config.get("client_secret"))

        data                = {"grant_type": "client_credentials",
                               "scope": "public"}

        authentication_response = requests.post(AUTH_URL,
                                                headers=header,
                                                data=json.dumps(data),
                                                auth=HTTPBasicAuth(client_id, client_secret))

        if authentication_response.status_code == 200:
            authentication_response_json = authentication_response.json()
            return {"x-ratelimit-limit"     : authentication_response.headers.get("x-ratelimit-limit"),
                    "x-ratelimit-remaining" : authentication_response.headers.get("x-ratelimit-remaining"),
                    "expires_in"            : authentication_response_json.get("expires_in"),
                    "access_token"          : authentication_response_json.get("access_token")}
        else:
            # TODO Add exception json here
            pass





