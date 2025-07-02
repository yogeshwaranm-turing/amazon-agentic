import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateDeposit(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        account_id: str, 
        amount: float, 
        source: str
    ) -> str:
        txs = data["transactions"]
        
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys()]
        
        new_tx = max(existing, default=0) + 1
        tx_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{new_tx}"
        
        tx = {
            "transaction_id": tx_id,
            "account_id": account_id,
            "type": "deposit",
            "amount": amount,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "related_id": None,
            "description": f"Deposit via {source}",
            "status": "completed",
            "fee": 0.00,
            "running_balance": None,  # This would need to be calculated
            "geo_location": {
                "lat": None,
                "lng": None,
                "city": None,
                "country": "USA"
            },
            "reference_id": None,
            "tags": ["deposit"],
            "notes": None,
            "merchant": None,
            "channel": source
        }
        
        txs[tx_id] = tx
        deps = data["deposits"]
        
        dep_id = f"DEPST-{new_tx}"
        dep = {
            "deposit_id": dep_id,
            "transaction_id": tx_id,
            "account_id": account_id,
            "source": source,
            "deposit_method": source,
            "channel": source,
            "amount": amount,
            "currency": "USD",
            "received_at": tx["timestamp"],
            "status": "completed",
            "cleared_at": tx["timestamp"],
            "fee": tx["fee"],
            "geo_location": tx["geo_location"],
            "notes": tx["notes"],
            "originator": {
            "company": None,
            "reference": None
            }
        }
        
        deps[dep_id] = dep
        
        return json.dumps(dep)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_deposit",
                "description": "Record a deposit to an account.",
                "parameters": {
                    "type":"object",
                    "properties": {
                        "account_id": {
                            "type":"string"
                        },
                        "amount": {
                            "type":"number"
                        },
                        "source": {
                            "type": "string",
                            "enum": ["branch", "mobile", "online", "ATM"]
                        }
                    },
                    "required": ["account_id", "amount", "source"]
                }
            }
        }