import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class PayInvoice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        invoice_id: str, 
        account_id: str, 
        amount: float
    ) -> str:
        invoices = data["invoices"]
        inv = invoices.get(invoice_id)
        
        if not inv:
            raise Exception("NotFound")
        
        if inv.get("status") == "paid":
            raise Exception("Invoice already paid")
        
        # create transaction
        txs = data.setdefault("Transactions", {})
        existing = [int(t.replace("TXN-", "").split('-')[-1]) for t in txs.keys()]
        new_tx = max(existing, default=0) + 1
        tx_id = f"TXN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{new_tx}"
        
        tx = {
            "transaction_id": tx_id,
            "account_id": account_id,
            "type": "withdrawal",
            "amount": amount,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "related_id": invoice_id,
            "description": f"Payment for invoice {invoice_id}",
            "status": "completed",
            "fee": 0.0,
            "running_balance": None,
            "geo_location": None,
            "reference_id": None,
            "tags": ["invoice_payment"],
            "notes": None,
            "merchant": None,
            "channel": "api"
        }
        txs[tx_id] = tx
        
        # update invoice
        if amount >= inv.get("amount_due", 0):
            inv["status"] = "paid"

        return json.dumps({
            "invoice": inv, 
            "payment_transaction": tx
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "pay_invoice",
                "description": "Record payment toward an invoice.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string"
                        },
                        "account_id": {
                            "type": "string"
                        },
                        "amount": {
                            "type": "number"
                        }
                    },
                    "required": ["invoice_id", "account_id", "amount"]
                }
            }
        }