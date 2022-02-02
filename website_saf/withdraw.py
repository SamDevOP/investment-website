import requests
from auth import MpesaBase
from mpesa_credentials import *
till="174379"

queue_timeout_url="https://mydomain.com/path"
result_url="https://mydomain.com/path"

class B2C(MpesaBase):
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

    def transact(
        self,
        initiator_name=None,
        security_credential=SECURITY_CREDENTIAL,
        command_id="PromotionPayment",
        amount=None,
        party_a=till,
        party_b=None,
        remarks="Withdrawal",
        queue_timeout_url=queue_timeout_url,
        result_url=result_url,
        occassion="Withdrawal",
    ):
        """This method uses Mpesa's B2C API to transact between an M-Pesa short code to a phone number registered on M-Pesa..

        **Args:**

        - `initiator_name` (str): Username used to authenticate the transaction.

        - `security_credential` (str): Generate from developer portal

        - `command_id` (str): Options: SalaryPayment, BusinessPayment, PromotionPayment

        - `amount`(str): Amount.

        - `party_a` (int): Organization/MSISDN making the transaction - Shortcode (6 digits) - MSISDN (12 digits).

        - `party_b` (int): MSISDN receiving the transaction (12 digits).

        - `remarks` (str): Comments that are sent along with the transaction(maximum 100 characters).

        - `account_reference` (str): Use if doing paybill to banks etc.

        - `queue_timeout_url` (str): The url that handles information of timed out transactions.

        - `result_url` (str): The url that receives results from M-Pesa api call.

        - `ocassion` (str):



        **Returns:**

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.

        - `ConversationID` (str): The unique request ID returned by mpesa for each request made

        - `ResponseDescription` (str): Response Description message



        """

        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occassion": occassion,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(
            base_safaricom_url, "/mpesa/b2c/v1/paymentrequest")
        try:
            r = requests.post(saf_url, headers=headers, json=payload)
        except Exception as e:
            r = requests.post(saf_url, headers=headers,
                              json=payload, verify=False)
        print(r.text)
        return r.json()
