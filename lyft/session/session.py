import json
import requests
from requests.auth import HTTPBasicAuth

from lyft.util.url_util import PUBLIC_AUTH_URL, AUTH_REVOKE_URL


class Session:

    def __init__(self, config, refresh_token, sandbox_mode=False):
        """This class is used to refresh or revoke the authentication or access token

        :param refresh_token: Token we get after the user authorizes the application
        """
        self.refresh_token  = refresh_token
        self.__sandbox_mode = sandbox_mode

        if config.get("client_id") is not None and config.get("client_secret") is not None:
            self.__config       = config
        else:
            raise ValueError("client id or client secret is None")

    def refresh_access_token(self):
        """Method to refresh the access token

        :return: New Acceess token JSON Object
        """
        header = {"content-type": "application/json"}
        data   = {"grant_type": "refresh_token", "refresh_token": self.refresh_token()}

        client_id = self.__config.get("client_id")
        if self.__sandbox_mode is False:
            client_secret = self.__config.get("client_secret")
        else:
            client_secret = "SANDBOX-{}".format(self.__config.get("client_secret"))

        refresh_token_response = requests.post(PUBLIC_AUTH_URL,
                                               headers=header,
                                               data=json.dumps(data),
                                               auth=HTTPBasicAuth(client_id, client_secret))

        if refresh_token_response.status_code == 200:
            refresh_token_response_json = refresh_token_response.json()
            return json.dumps({"access_token"          : refresh_token_response_json.get("access_token"),
                               "token_type"            : refresh_token_response_json.get("token_type"),
                               "expires_in"            : refresh_token_response_json.get("expires_in"),
                               "scope"                 : refresh_token_response_json.get("scope"),
                               "x-ratelimit-remaining" : refresh_token_response.headers.get("x-ratelimit-remaining"),
                               "x-ratelimit-limit"     : refresh_token_response.headers.get("x-ratelimit-limit")
                               })
        else:
            raise Exception(refresh_token_response.text)

    def revoke_token(self):
        """Removes the user refresh token

        :return: Success JSON Object
        """
        header = {"content-type": "application/json"}
        data   = {"token"       : self.refresh_token}

        client_id = self.__config.get("client_id")
        if self.__sandbox_mode is False:
            client_secret = self.__config.get("client_secret")
        else:
            client_secret = "SANDBOX-{}".format(self.__config.get("client_secret"))

        revoke_token_response = requests.post(AUTH_REVOKE_URL,
                                              data=json.dumps(data),
                                              headers=header,
                                              auth=HTTPBasicAuth(client_id, client_secret))
        if revoke_token_response.status_code == 200:
            return json.dumps({"status": True})
        else:
            raise Exception(revoke_token_response.text)
