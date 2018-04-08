import json
import requests
from requests.auth import HTTPBasicAuth

from lyft.util.url_util import PUBLIC_AUTH_URL, USER_AUTH_URL


class LyftPublicAuth:
    def __init__(self, config, sandbox_mode=False):
        """Authentication class for the 2 legged flow. This calls does not need user data and can access the public
        endpoints directly with the client secret and client ID. After successful authentication it will retrurn the
        access token


        :param sandbox_mode: Set to True if you want a sandbox environment else False
        :param config: Dictionary of client_id and client_secret

        """
        self.__sandbox_mode = sandbox_mode
        self.__config = config

    def get_access_token(self):
        """Retrieves the access token along with the expiration time and rate limiting data in a dictionary

        :return: authentication_object
        :rtype: dict
        """
        header = {"content-type": "application/json"}

        client_id       = self.__config.get("client_id")
        if self.__sandbox_mode is False:
            client_secret   = self.__config.get("client_secret")
        else:
            client_secret   = "SANDBOX-{}".format(self.__config.get("client_secret"))

        data = {"grant_type": "client_credentials",
                "scope": "public"}

        authentication_response = requests.post(PUBLIC_AUTH_URL,
                                                headers=header,
                                                data=json.dumps(data),
                                                auth=HTTPBasicAuth(client_id, client_secret))

        if authentication_response.status_code == 200:
            authentication_response_json = authentication_response.json()
            return {"x-ratelimit-limit"     : authentication_response.headers.get("x-ratelimit-limit"),
                    "x-ratelimit-remaining" : authentication_response.headers.get("x-ratelimit-remaining"),
                    "expires_in"            : authentication_response_json.get("expires_in"),
                    "access_token"          : authentication_response_json.get("access_token"),
                    "token_type"            : authentication_response_json.get("token_type")}

        else:
            return authentication_response.json()


class LyftUserAuth:

    def __init__(self, config, scopes, state, sandbox_mode=False):
        """Authentcation class for the 3 legged flow.

        :param sandbox_mode: Set to True if you want a sandbox environment else False
        :param config: Dictionary of client_id and client_secret
        :param scopes: List of scopes that you need to give get from the user
        :param state: A payload which will be passed back to your application through the redirect

        """
        self.__sandbox_mode = sandbox_mode
        self.__config       = config
        self.__scopes       = scopes
        self.__state        = state

    def get_authorization_uri(self):
        """Returns the authorization URI that will be presented to the customer to authenticate. Present this URL in the
        application. The user will see information about your application, along with the list of permissions your
        application is requesting. The user can indicate whether Lyft should grant access to your application or not.
        As soon as the user authenticates you will be given an authorization code.

        From the docs, (https://developer.lyft.com/docs/authentication)
        If the Lyft user grants your application access to the requested permissions, Lyft will issue a 302 redirect to
        the Redirect URI you've set up with Lyft, along with an authorization code as a URL parameter. The authorization
        code should be used in the next step. It is a one-time use code, which expires after 10 minutes.
        It will appear on your server like this:

        GET 'your-redirect-uri/?code=<authorization_code>'

        :return: URL: authorization URL that will be presented to user
        """
        client_id     = self.__config.get("client_id")
        if len(self.__scopes) > 0:
            scopes        = "%20".join(self.__scopes)
        else:
            return None

        if client_id is None or len(client_id) == 0:
            return None

        header = {"content-type": "application/json"}
        redirect_response = requests.get("{}?client_id={}&scope={}&state={}&response_type=code".format(USER_AUTH_URL,
                                                                                                       client_id,
                                                                                                       scopes,
                                                                                                       self.__state),
                                         headers=header
                                         )

        if redirect_response.status_code == 200:
            return redirect_response.url

        else:
            return redirect_response.json()

    def get_access_token(self, authorization_code):
        """We will use the authorization code that we will get after the user authenticates with the application to
        retrieve an access token to perform various operations related to your scope.

        :param authorization_code: Code to retrieve the access token
        :return: access token object
        """
        header = {"content-type": "application/json"}
        data   = {"grant_type": "authorization_code", "code": authorization_code}

        client_id = self.__config.get("client_id")

        if self.__sandbox_mode is False:
            client_secret = self.__config.get("client_secret")
        else:
            client_secret = "SANDBOX-{}".format(self.__config.get("client_secret"))

        authentication_response = requests.post(PUBLIC_AUTH_URL,
                                                headers=header,
                                                data=json.dumps(data),
                                                auth=HTTPBasicAuth(client_id, client_secret))

        if authentication_response.status_code == 200:
            authentication_response_json = authentication_response.json()
            return {"access_token"          : authentication_response_json.get("access_token"),
                    "refresh_token"         : authentication_response_json.get("refresh_token"),
                    "token_type"            : authentication_response_json.get("token_type"),
                    "expires_in"            : authentication_response_json.get("expires_in"),
                    "scope"                 : authentication_response_json.get("scope"),
                    "x-ratelimit-remaining" : authentication_response.headers.get("x-ratelimit-remaining"),
                    "x-ratelimit-limit"     : authentication_response.headers.get("x-ratelimit-limit")
                    }

        else:
            return authentication_response.json()
