import requests
from requests.auth import HTTPBasicAuth
from mpesa_credentials import *

class MpesaBase:
    def __init__(
        self,
        env="producti",
        app_key=CONSUMER_KEY,
        app_secret=CONSUMER_SECRET,
        sandbox_url="https://sandbox.safaricom.co.ke",
        live_url="https://api.safaricom.co.ke",
    ):
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.token = None

    def authenticate(self):
        """To make Mpesa API calls, you will need to authenticate your app. This method is used to fetch the access token
        required by Mpesa. Mpesa supports client_credentials grant type. To authorize your API calls to Mpesa,
        you will need a Basic Auth over HTTPS authorization token. The Basic Auth string is a base64 encoded string
        of your app's client key and client secret.

            **Args:**

                - `env` (str): Current app environment. Options: sandbox, live.

                - `app_key` (str): The app key obtained from the developer portal.

                - `app_secret` (str): The app key obtained from the developer portal.

                - `sandbox_url` (str): Base Safaricom sandbox url.

                - `live_url` (str): Base Safaricom live url.


            **Returns:**

                - `access_token` (str): This token is to be used with the Bearer header for further API calls to Mpesa.

            """
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        authenticate_uri = "/oauth/v1/generate?grant_type=client_credentials"
        authenticate_url = "{0}{1}".format(
            base_safaricom_url, authenticate_uri)
        
        print(authenticate_url)
        try:
            r = requests.get(
                authenticate_url, auth=HTTPBasicAuth(
                    self.app_key, self.app_secret)
            )
           
        except Exception as e:
            r = requests.get(
                authenticate_url,
                auth=HTTPBasicAuth(self.app_key, self.app_secret),
                verify=False,
            )

        print(r.text)
        return r.json()["access_token"]






