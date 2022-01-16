import base64
import requests
from auth import MpesaBase
from datetime import datetime
import time
from mpesa_credentials import *
#from test import *
till="174379"
class MpesaExpress(MpesaBase):
    def __init__(
        self,
        env="sandbox",
        app_key=CONSUMER_KEY,
        app_secret=CONSUMER_SECRET,
        sandbox_url="https://sandbox.safaricom.co.ke",
        live_url="https://api.safaricom.co.ke",
    ):
        MpesaBase.__init__(self, env, app_key, app_secret,
                           sandbox_url, live_url)
        self.authentication_token = self.authenticate()
#Till number 9309125
    def stk_push(
        self,
        business_shortcode=till,
        passcode=None,
        amount=None,
        callback_url='https://mydomain.com/path',
        reference_code="Peak Investors",
        phone_number=None,
        description="Peak Investors",
    ):
        """This method uses Mpesa's Express API to initiate online payment on behalf of a customer..

        **Args:**

        - `business_shortcode` (int): The short code of the organization.

        - `passcode` (str): Get from developer portal

        - `amount` (int): The amount being transacted

        - `callback_url` (str): A CallBack URL is a valid secure URL that is used to receive notifications from M-Pesa API.

        - `reference_code`: Account Reference: This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type.

        - `phone_number`: The Mobile Number to receive the STK Pin Prompt.

        - `description`: This is any additional information/comment that can be sent along with the request from your system. MAX 13 characters



        **Returns:**

        - `CustomerMessage` (str):

        - `CheckoutRequestID` (str):

        - `ResponseDescription` (str):

        - `MerchantRequestID` (str):

        - `ResponseCode` (str):


        """
        paskey=PASS_KEY
        time=datetime.now().strftime("%Y%m%d%H%M%S")
        encode_data = business_shortcode + paskey + time
        passkey  = base64.b64encode(encode_data.encode())
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": passkey.decode('utf-8'),#encoded.decode("utf-8"),
            "Timestamp": time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": reference_code,
            "TransactionDesc": description,
        }
        
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/stkpush/v1/processrequest"
        )
        
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
            
        except Exception as e:
            r = requests.post(saf_url, headers=headers,json=payload, verify=False)
        print(r.text)    
        return r.json()

    def query(self, business_shortcode=till, checkout_request_id=None, passcode=None):
        """This method uses Mpesa's Express API to check the status of a Lipa Na M-Pesa Online Payment..

        **Args:**

        - `business_shortcode` (int): This is organizations shortcode (Paybill or Buygoods - A 5 to 6 digit account number) used to identify an organization and receive the transaction.

        - `checkout_request_id` (str): This is a global unique identifier of the processed checkout transaction request.

        - `passcode` (str): Get from developer portal


        **Returns:**

        - `CustomerMessage` (str):

        - `CheckoutRequestID` (str):

        - `ResponseDescription` (str):

        - `MerchantRequestID` (str):

        - `ResponseCode` (str):


        """

        paskey=PASS_KEY
        time=datetime.now().strftime("%Y%m%d%H%M%S")
        encode_data = business_shortcode + paskey + time
        passkey  = base64.b64encode(encode_data.encode())
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": passkey.decode('utf-8'),  #encoded.decode("utf-8"),
            "Timestamp": time,
            "CheckoutRequestID": checkout_request_id,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/stkpushquery/v1/query")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception as e:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        print(r.text)
        return r.json()

# lipa=MpesaExpress()

# stkpush=lipa.stk_push(amount="1",phone_number="254798766620")

# time.sleep(10)
# check_stkpush=lipa.query(checkout_request_id=stkpush["CheckoutRequestID"])
