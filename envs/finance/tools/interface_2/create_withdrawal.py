import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateWithdrawal(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        account_id: str, 
        amount: float, 
        method: str
    ) -> str:
        txs = data["transactions"]
        
        if method not in ["ATM", "teller", "online"]:
            raise ValueError(f"Invalid withdrawal method: {method}. Must be one of ['ATM', 'teller', 'online'].")
        
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys()]
        new_tx = max(existing, default=0) + 1
        tx_id = f"TXN-{datetime.now().strftime('%Y%m%d')}-{new_tx}"
        
        tx = {
            "transaction_id": tx_id,
            "account_id": account_id,
            "type": "withdrawal",
            "amount": amount,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "related_id": None,
            "description": f"{method.capitalize()} withdrawal",
            "status": "completed",
            "fee": 0.00,
            "running_balance": None,  # This would need to be calculated
            "geo_location": None,
            "reference_id": None,
            "tags": ["withdrawal", method.lower()],
            "notes": None,
            "merchant": None,
            "channel": method.lower()
        }
        
        txs[tx_id] = tx
        
        wds = data["withdrawals"]
        wd_id = f"WDWL-{new_tx}"
        
        wd = {
            "withdrawal_id": wd_id,
            "transaction_id": tx_id,
            "method": method,
            "channel": tx["channel"],
            "processed_at": tx["timestamp"],
            "amount": amount,
            "currency": tx["currency"],
            "fee": tx["fee"],
            "status": tx["status"],
            "running_balance": tx["running_balance"],
            "geo_location": tx["geo_location"],
            "notes": tx["notes"],
            "teller_details": None,
            "employee_id": None
        }
        
        wds[wd_id] = wd
        
        return json.dumps(wd)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_withdrawal",
                "description": "Record a withdrawal from an account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string"
                        },
                        "amount": {
                            "type": "number"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["ATM", "teller", "online"]
                        }
                    },
                    "required": ["account_id", "amount", "method"]
                }
            }
        }