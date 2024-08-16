# stitch-money-api
A Python package for processing digitial wallets payments via the Stitch API. 
For the complete integration guide, visit [docs.stitch.money](https://docs.stitch.money/payment-products/payins/wallets/integration-process).

# Installation

```bash
$ pip3 install stitch-money-api
```

## Usage

```python
import json
import os
from stitch.payins import Wallets
from stitch.utils.types import Wallet, Currency
import uuid
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("STITCH_CLIENT_ID")
client_secret = os.getenv("STITCH_CLIENT_SECRET")

# Initialise SDK
stitch_sdk = Wallets(client_id, client_secret, 'merchant.energy.bigbag')

# Payment Verification (Web Only)
session = stitch_sdk.verify(
    Wallet.APPLE_PAY, 1, Currency.ZAR, 'https://apple-pay-gateway.apple.com/paymentservices/startSession', 'TAL', 'bigbag.money')
print(session)

# Payment Creation
transaction = stitch_sdk.create(
    Wallet.GOOGLE_PAY, json.dumps({"data": "sample"}), 1, Currency.ZAR, 'PythonSDK', str(uuid.uuid4()))
print(transaction)
```

# License

The stitch-money-api package is open source and available under the MIT license. See the LICENSE file for more information.