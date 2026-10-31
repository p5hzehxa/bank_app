from flask import Flask, render_template
import jwt, time, requests, os
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

APP_ID = os.environ.get("APP_ID", "664c0c2d-ef9a-4bd2-a85f-91e22bf6f48a")
ACCOUNT_UID = os.environ.get("ACCOUNT_UID", "c9b98eb9-e0b5-4b41-85f8-273f55ce6889")

def get_token():
    key_data = os.environ.get("PRIVATE_KEY")
    if key_data:
        private_key = serialization.load_pem_private_key(key_data.encode('utf-8'), password=None)
    else:
        with open("private.key", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
            
    now = int(time.time())
    payload = {"iss": "enablebanking.com", "aud": "api.enablebanking.com", "iat": now, "exp": now + 3600}
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": APP_ID})

@app.route('/')
def index():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    bal_res = requests.get(f"https://api.enablebanking.com/accounts/{ACCOUNT_UID}/balances", headers=headers).json()
    tx_res = requests.get(f"https://api.enablebanking.com/accounts/{ACCOUNT_UID}/transactions", headers=headers).json()
    
    return render_template('index.html', balances=bal_res.get('balances', []), transactions=tx_res.get('transactions', []))

if __name__ == '__main__':
    main.py(host='0.0.0.0', port=5000)
