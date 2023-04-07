import requests
from auth import MpesaBase

from mpesa_credentials import *


class C2B(MpesaBase):
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

    def register(
        self,
        shortcode="601426",
        response_type="Completed",
        confirmation_url="https://5d1b-197-232-128-93.ngrok.io/v1/payment_notification",
        validation_url="https://5d1b-197-232-128-93.ngrok.io/v1/payment_notification",
    ):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.

        **Args:**

        - `shortcode` (int): The short code of the organization.

        - `response_type` (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.

        - `confirmation_url` (str): Confirmation URL for the client.

        - `validation_url` (str): Validation URL for the client.



        **Returns:**

        - `OriginatorConversationID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message



        """

        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        

        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/c2b/v1/registerurl")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception as e:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()

    def simulate(
        self,
        shortcode="601426",
        command_id='CustomerPayBillOnline',
        amount=1,
        msisdn=254708374149,
        bill_ref_number='Test001'
    ):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.

        **Args:**

        - `shortcode` (int): The short code of the organization.

        - `command_id` (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.

        - `amount` (int): The amount being transacted

        - `msisdn` (int): Phone number (msisdn) initiating the transaction MSISDN(12 digits)

        - `bill_ref_number`: Optional



        **Returns:**

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message



        """

        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/simulate")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception as e:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        return r.json()


con='https://moibenconnections-stage-7633966.dev.odoo.com/v1/payment_notification'
val=None

c_2_b =C2B()

#res = c_2_b.register(shortcode=int(Shortcode),response_type='Completed',confirmation_url=con,validation_url=val)
sim=c_2_b.simulate()
#res = c_2_b.register()
print(sim)
