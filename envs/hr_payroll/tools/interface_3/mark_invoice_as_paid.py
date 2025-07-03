
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class MarkInvoiceAsPaid(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_id: str) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})

        if invoice_id not in invoices:
            raise ValueError("Invoice not found")
        if payment_id not in payments:
            raise ValueError("Payment not found")
        if payments[payment_id]["invoice_id"] != invoice_id:
            raise ValueError("Payment does not match the invoice")

        invoices[invoice_id]["status"] = "paid"
        return json.dumps({"invoice_id": invoice_id, "status": "paid"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "mark_invoice_as_paid",
                "description": "Marks an invoice as paid using a payment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "ID of the invoice to be marked as paid"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "ID of the payment used to mark the invoice as paid"
                        }
                    },
                    "required": ["invoice_id", "payment_id"]
                }
            }
        }
