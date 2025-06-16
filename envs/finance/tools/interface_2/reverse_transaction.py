import json
from typing import Any, Dict
from datetime import datetime, timezone
from faker import Faker
from tau_bench.envs.tool import Tool

fake = Faker()

class ReverseTransaction(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      transaction_id: str
    ) -> str:
        txns = data["transactions"]
        txn = txns.get(transaction_id)
        
        if not txn:
            raise KeyError(f"Transaction {transaction_id} not found")
          
        txn["status"] = "reversed"
        txn["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        refunds = data["refunds"] if "refunds" in data else {}
        
        if not refunds:
            data["refunds"] = refunds
            
        suffix = transaction_id.split("-")[-1]
        refund_id = f"RFND-{suffix}"
        
        refund = {
          "refund_id": refund_id,
          "transaction_id": transaction_id,
          "refund_method": "branch",
          "refund_channel": "branch",
          "processed_at": datetime.now(timezone.utc).isoformat(),
          "status": "completed",
          "original_amount": txn["amount"],
          "refund_amount": txn["amount"],
          "reason": "billing_error",
          "currency": "USD",
          "fee_refunded": 0.0,
          "reversal_reference": f"RL-{suffix}",
          "initiated_by": {"user_id": "CUST415020"},
          "approved_by": "CUST896615",
          "approved_at": datetime.now(timezone.utc).isoformat(),
          "gl_account": "ACCOUNTS_PAYABLE",
          "tax_code": "REFUND-ZY#",
          "customer_notes": "Identify able attorney quality."
        }
        refunds[refund_id] = refund
        
        return json.dumps(txn)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "reverse_transaction",
            "description": "Mark a transaction reversed and generate refund.",
            "parameters": {
              "type": "object",
              "properties": { "transaction_id": { "type": "string" } },
              "required": ["transaction_id"]
            }
          }
        }
