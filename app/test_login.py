import requests
import pyotp

# Replace these with your actual credentials
client_code = "S295624"
password = "5451"
totp_secret = "MGSIZURVEDJQVUH7ANKNVXCX4A"  # This is the secret key, not the current 6-digit code

totp = pyotp.TOTP(totp_secret).now()

headers = {
    "Content-type": "application/json",
    "X-ClientLocalIP": "127.0.0.1",
    "X-ClientPublicIP": "106.193.147.98",  # Optional, use your actual IP if needed
    "X-MACAddress": "50:91:e3:21:d3:09",    # Optional
    "Accept": "application/json",
    "X-PrivateKey": "NuzOVu1i",
    "X-UserType": "USER",
    "X-SourceID": "WEB"
}

payload = {
    "clientcode": client_code,
    "password": password,
    "totp": totp
}

try:
    response = requests.post(
        "https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/loginByPassword",
        json=payload,
        headers=headers,
        timeout=10  # seconds
    )
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.ConnectTimeout:
    print("❌ Connection timed out.")
except Exception as e:
    print("❌ Error:", e)
