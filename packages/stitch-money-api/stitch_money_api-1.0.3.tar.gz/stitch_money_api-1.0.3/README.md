# stitch-money-api
A Python package for processing digitial wallets payments via the Stitch API. 
For the complete integration guide, visit [docs.stitch.money](http://localhost:3000/payment-products/payins/wallets/introduction).

# Installation

```bash
$ pip3 install stitch-money-api
```

## Usage

### Payment Initiation

```python
from pyramid.view import view_config
from pyramid.response import Response
from stitch.utils.types import Wallet, Currency, Transaction
import json
import uuid

@view_config(route_name='create', request_method='POST', renderer='json')
def create_apple_pay_payment(request) -> Transaction:
    data = request.json_body
    payment_token = data.get('payment_token')

    nonce = str(uuid.uuidv4())
    quantity = 1
    currency = Currency.ZAR
    reference = "StitchTest"

    transaction = sdk.create(
        Wallet.APPLE_PAY,
        payment_token,
        quantity,
        currency,
        nonce,
        reference
    )

    return transaction
```


### Merchant Verification
Note this is not required for mobile (native) app integrations. 

```python
from pyramid.view import view_config
from pyramid.response import Response
from stitch.utils.types import Wallet, Currency, Session
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("STITCH_CLIENT_ID")
client_secret = os.getenv("STITCH_CLIENT_SECRET")

sdk = Wallets(client_id, client_secret, 'merchant.money.stitch')

@view_config(route_name='verify', request_method='POST', renderer='json')
def create_samsung_pay_payment(request) -> Session:
    data = request.json_body
    verification_url = data.get('verification_url') # 'https://apple-pay-gateway.apple.com/paymentservices/startSession'
    initiative_context = data.get('initiative_context') # secure.stitch.money (FQDN)

    displayName = "Stitch"

    session = sdk.verify(
        Wallet.APPLE_PAY,
        quantity,
        currency,
        verification_url,
        displayName,
        initiative_context
    )

    return session
```

# License

The stitch-money-api package is open source and available under the MIT license. See the LICENSE file for more information.