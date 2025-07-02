# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "accounts.json")) as f:
        account_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "assets.json")) as f:
        asset_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "audit_trails.json")) as f:
        audit_trail_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "authorizations.json")) as f:
        authorization_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "deposits.json")) as f:
        deposit_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "depreciations.json")) as f:
        depreciation_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "disposals.json")) as f:
        disposal_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "invoices.json")) as f:
        invoice_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "loans.json")) as f:
        loan_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "refunds.json")) as f:
        refund_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "transactions.json")) as f:
        transaction_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "users.json")) as f:
        user_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "withdrawals.json")) as f:
        withdrawal_data = json.load(f)
    return {
        "accounts": account_data,
        "assets": asset_data,
        "audit_trails": audit_trail_data,
        "authorizations": authorization_data,
        "deposits": deposit_data,
        "depreciations": depreciation_data,
        "disposals": disposal_data,
        "invoices": invoice_data,
        "loans": loan_data,
        "refunds": refund_data,
        "transactions": transaction_data,
        "users": user_data,
        "withdrawals": withdrawal_data,
    }
