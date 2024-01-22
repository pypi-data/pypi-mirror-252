# pytallyerp

## Usage

```python

import tallyerp
gateway = tallyerp.connect("http://192.168.0.1:9000")
gateway.master.createLedger(
    name='Ledger name', 
    parent='Sundry Debtor', 
    openingBalance=1000
)

```