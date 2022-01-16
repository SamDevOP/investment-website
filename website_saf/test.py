import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64

def get_mpesa_token():

    consumer_key = "O8iX4i9GJD2Jky0xckoNJ86t0Dm5njv1"
    consumer_secret = "MIdpuRk1lvGcsYu9"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests liblary
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # return access_token from response
    return r.json()['access_token']

access_token=get_mpesa_token()



headers = { "Authorization": f"Bearer {access_token}"  }
paskey="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
bus_short="174379"
time=datetime.now().strftime("%Y%m%d%H%M%S")


      #  """ make and stk push to daraja API"""

encode_data = bus_short + paskey + time

        
        # encode business_shortcode, online_passkey and current_time (yyyyMMhhmmss) to base64
passkey  = base64.b64encode(encode_data.encode())


time=datetime.now().strftime("%Y%m%d%H%M%S")


payload = {

    "BusinessShortCode": "174379",
    "Password": passkey.decode('utf-8'),
    "Timestamp": time,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": "200",
    "PartyA": "254798766620",
    "PartyB": "174379",
    "PhoneNumber": "254798766620",
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
  }

response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
print(response.text)
#print(response.text.encode('utf8'))