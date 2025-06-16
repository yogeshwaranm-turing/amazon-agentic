import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvoicePayment(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      invoice_id: str, 
      amount: float, 
      account_id: str
    ) -> str:
        # Create payment transaction and apply to invoice
        invs = data.get("invoices", {})
        invoice = invs.get(invoice_id)
        
        if not invoice:
            raise KeyError(f"Invoice {invoice_id} not found")
          
        # Create transaction
        txns = data.setdefault("transactions", {})
        txn_id = f"TXN-{len(txns)+1:06d}"
        now = datetime.now(timezone.utc).isoformat()
        txn = {
            "transaction_id": txn_id,
            "account_id": account_id,
            "type": "payment",
            "amount": amount,
            "currency": invoice.get("currency", "USD"),
            "timestamp": now,
            "related_id": invoice_id,
            "description": f"Payment for invoice {invoice_id}",
            "status": "posted",
            "fee": 0.0,
            "running_balance": None,
            "geo_location": {},
            "reference_id": None,
            "tags": [],
            "notes": None,
            "originator": {},
            "channel": "payment"
        }
        
        txns[txn_id] = txn
        # Update invoice
        invoice["amount_paid"] = invoice.get("amount_paid",0.0) + amount
        if invoice["amount_paid"] >= invoice["total_amount"]:
            invoice["status"] = "paid"
            invoice["paid_at"] = now
            
        return json.dumps({"transaction": txn, "invoice": invoice})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"create_invoice_payment",
            "description":"Record a payment towards an invoice and create a payment transaction.",
            "parameters":{
                "type":"object",
                "properties":{
                    "invoice_id":{"type":"string"},
                    "amount":{"type":"number"},
                    "account_id":{"type":"string"}
                },
                "required":["invoice_id","amount","account_id"]
            }
        }}