
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitInvoicePayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_id: str) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})

        if invoice_id not in invoices:
            raise ValueError("Invoice not found")
        if payment_id not in payments:
            raise ValueError("Payment not found")

        invoice = invoices[invoice_id]
        payment = payments[payment_id]

        if payment["invoice_id"] != invoice_id:
            raise ValueError("Payment doesn't match invoice")

        invoice["status"] = "paid"
        return json.dumps({"invoice_id": invoice_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_invoice_payment",
                "description": "Marks an invoice as paid if payment matches invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "The invoice to update"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment ID associated with invoice"
                        }
                    },
                    "required": ["invoice_id", "payment_id"]
                }
            }
        }
