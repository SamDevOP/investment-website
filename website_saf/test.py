import requests
from datetime import datetime
headers = {

  'Content-Type': 'application/json',

  'Authorization': 'Bearer IinSXSsUoaJK5gy81PGLo7vVoEJN'

}

time=datetime.now().strftime("%Y%m%d%H%M%S")
payload = {

    "BusinessShortCode": 174379,

    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwMTA1MjIwMjI3",

    "Timestamp": time,

    "TransactionType": "CustomerPayBillOnline",

    "Amount": 1,

    "PartyA": 254798766620,

    "PartyB": 174379,

    "PhoneNumber": 254798766620,

    "CallBackURL": "https://mydomain.com/path",

    "AccountReference": "CompanyXLTD",

    "TransactionDesc": "Payment of X" 

  }

response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)

print(response.text.encode('utf8'))