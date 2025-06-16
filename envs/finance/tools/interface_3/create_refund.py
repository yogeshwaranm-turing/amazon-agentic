import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateRefund(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      transaction_id: str, 
      reason: str
    ) -> str:
        refunds = data["refunds"]
        new_id = f"RFND-{len(refunds)+1:06d}"
        txn = data.get("transactions", {}).get(transaction_id)
        
        if not txn:
            raise KeyError(f"Transaction {transaction_id} not found")
          
        refund = {
            "refund_id": new_id,
            "transaction_id": transaction_id,
            "refund_method": "branch",
            "refund_channel": "branch",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "status": "completed",
            "original_amount": txn["amount"],
            "refund_amount": txn["amount"],
            "reason": reason,
            "currency": txn["currency"],
            "fee_refunded": txn.get("fee", 0.0),
            "reversal_reference": f"RL-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{new_id.split('-')[1]}",
            "initiated_by": {
              "user_id": txn.get("customer_id", "UNKNOWN")
            },
            "approved_by": txn.get("approver_id", "UNKNOWN"),
            "approved_at": datetime.now(timezone.utc).isoformat(),
            "gl_account": txn.get("gl_account", "ACCOUNTS_PAYABLE"),
            "tax_code": txn.get("tax_code", "REFUND-KR#"),
            "customer_notes": txn.get("customer_notes", "")
        }
        refunds[new_id] = refund
        
        return json.dumps(refund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_refund",
                "description": "Initiate a refund for a transaction.",
                "parameters": {
                    "type": "object",
                    "properties": {"transaction_id": {"type": "string"}, "reason": {"type": "string"}},
                    "required": ["transaction_id", "reason"]
                }
            }
        }