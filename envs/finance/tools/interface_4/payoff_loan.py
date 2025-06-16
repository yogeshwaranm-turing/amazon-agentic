import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class PayoffLoan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        loan_id: str, 
        account_id: str, 
        payoff_amount: float
    ) -> str:
        loans = data["loans"]
        loan = loans.get(loan_id)
        if not loan:
            raise Exception("NotFound")
        
        txs = data["transactions"]
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys()]
        new_tx = max(existing, default=0) + 1
        
        tx_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{new_tx}"
        tx = {
            "transaction_id": tx_id,
            "account_id": account_id,
            "type": "withdrawal",
            "amount": payoff_amount,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "related_id": loan_id,
            "description": f"Loan payoff for {loan_id}",
            "status": "completed",
            "fee": 0.0,
            "running_balance": None,
            "geo_location": None,
            "reference_id": None,
            "tags": ["loan_payoff"],
            "notes": None,
            "merchant": None,
            "channel": "system"
        }
        
        txs[tx_id] = tx
        loan["status"] = "paid_off"
        
        return json.dumps({
            "loan_id": loan_id, 
            "payoff_transaction": tx, 
            "status": loan["status"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "payoff_loan",
                "description": "Record payoff of a loan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "loan_id": {
                            "type": "string"
                        },
                        "account_id": {
                            "type": "string"
                        },
                        "payoff_amount": {
                            "type": "number"
                        }
                    },
                    "required": ["loan_id", "account_id", "payoff_amount"]
                }
            }
        }