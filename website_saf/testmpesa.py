from base64 import b64encode
import requests
from mpesa_credentials import *

def register():
        
    # Define the API endpoint
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    # Define the request payload
    payload = {
        "ShortCode": "<your M-Pesa short code>",
        "ResponseType": "Completed",
        "ConfirmationURL": "<your confirmation URL>",
        "ValidationURL": "<your validation URL>"
    }

    # Define the headers for the API request
    headers = {
        "Authorization": "Bearer <your access token>",
        "Content-Type": "application/json"
    }

    # Make the API call
    response = requests.post(url, json=payload, headers=headers)

    # Print the API response
    print(response.json())

def get_auth():


    # Define the API endpoint
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # Define the API credentials
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET

    # Define the headers for the API request
    headers = {
        "Authorization": "Basic <base64-encoded consumer key and secret>",
        "Content-Type": "application/json"
    }

    # Encode the consumer key and secret in base64
    auth = f"{consumer_key}:{consumer_secret}"
    base64_auth = b64encode(auth.encode("utf-8")).decode("utf-8")

    # Add the base64-encoded credentials to the headers
    headers["Authorization"] = f"Basic {base64_auth}"

    # Make the API call
    response = requests.post(url, headers=headers)

    # Print the API response
    print(response.json())

get_auth()

