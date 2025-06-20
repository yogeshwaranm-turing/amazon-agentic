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
        txs = data["transactions"]
        
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys()]
        next_id = max(existing, default=0) + 1
        dt = datetime.now(timezone.utc).isoformat()
        
        # Find current balance of from_account
        from_balance = next(
            (tx["running_balance"] for tx in reversed(txs.values()) 
                if tx["account_id"] == from_account_id), 
            0.0
        )
        
        # Find current balance of to_account
        to_balance = next(
            (tx["running_balance"] for tx in reversed(txs.values()) 
                if tx["account_id"] == to_account_id), 
            0.0
        )
        
        debit_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{next_id}"
        credit_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{next_id+1}"
        
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
                "description": "Automically transfer funds between two accounts.",
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