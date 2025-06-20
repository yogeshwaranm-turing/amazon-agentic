import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class TransferFunds(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        from_account_id: str, 
        to_account_id: str, 
        amount: float, 
        currency: str = "USD"
    ) -> str:
        accounts = data["accounts"]
        txs = data["transactions"]
        
        from_account = accounts.get(from_account_id)
        to_account = accounts.get(to_account_id)
        if from_account is None or to_account is None:
            raise ValueError("Account not found.")
        
        # Get available balances
        from_balance = from_account["balances"]["available"]
        to_balance = to_account["balances"]["available"]
        
        if from_balance < amount:
            raise ValueError("Insufficient funds in the source account.")
        
        # Update account balances
        from_account["balances"]["available"] -= amount
        to_account["balances"]["available"] += amount
        
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys() if t.startswith("TXN-")]
        next_id = max(existing, default=0) + 1
        dt = datetime.now(timezone.utc).isoformat()
        
        debit_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{next_id}"
        credit_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{next_id+1}"
        
        # update the accounts in the data
        accounts[from_account_id] = from_account
        accounts[to_account_id] = to_account
        
        debit = {
            "transaction_id": debit_id,
            "account_id": from_account_id,
            "type": "withdrawal",
            "amount": amount,
            "currency": currency,
            "timestamp": dt,
            "related_id": credit_id,
            "description": f"Transfer to account {to_account_id}",
            "status": "completed",
            "fee": 0.0,
            "running_balance": from_balance - amount,
            "geo_location": None,
            "reference_id": None,
            "tags": ["transfer"],
            "notes": None,
            "merchant": None,
            "channel": "api"
        }
        
        credit = {
            "transaction_id": credit_id,
            "account_id": to_account_id,
            "type": "deposit",
            "amount": amount,
            "currency": currency,
            "timestamp": dt,
            "related_id": debit_id,
            "description": f"Transfer from account {from_account_id}",
            "status": "completed",
            "fee": 0.0,
            "running_balance": to_balance + amount,
            "geo_location": None,
            "reference_id": None,
            "tags": ["transfer"],
            "notes": None,
            "merchant": None,
            "channel": "api"
        }
        
        txs[debit_id] = debit
        txs[credit_id] = credit
        
        return json.dumps({
            "debit_transaction": debit, 
            "credit_transaction": credit
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_funds",
                "description": "Automatically transfer funds between two accounts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_account_id": {
                            "type": "string"
                        },
                        "to_account_id": {
                            "type": "string"
                        },
                        "amount": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        }
                    },
                    "required": ["from_account_id", "to_account_id", "amount"]
                }
            }
        }