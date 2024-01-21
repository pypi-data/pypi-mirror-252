# pytallyerp

## Usage

```python

import tallyerp
gateway = tallyerp.connect()
gateway.master.createLedger(
    name='Ledger name', 
    parent='Sundry Debtor', 
    openingBalance=1000
)

```