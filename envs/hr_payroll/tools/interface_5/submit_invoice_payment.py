import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitInvoicePayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str,
        payment_id: str,
        worker_id: str = None,
        amount: float = None,
        issue_date: str = None,
        due_date: str = None,
        status: str = None,
        currency: str = None,
        organization_id: str = None
    ) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})

        if invoice_id not in invoices:
            raise ValueError("Invoice not found")
        if payment_id not in payments:
            raise ValueError("Payment not found")

        invoice = invoices[invoice_id]
        payment = payments[payment_id]

        if payment.get("invoice_id") != invoice_id:
            raise ValueError("Payment does not match invoice")

        # Update invoice fields if provided
        if worker_id is not None:
            invoice["worker_id"] = worker_id
        if amount is not None:
            invoice["amount"] = round(amount, 2)
        if issue_date is not None:
            invoice["issue_date"] = issue_date
        if due_date is not None:
            invoice["due_date"] = due_date
        if status is not None:
            invoice["status"] = status
        else:
            invoice["status"] = "paid"  # fallback if no status explicitly provided
        if currency is not None:
            invoice["currency"] = currency
        if organization_id is not None:
            invoice["organization_id"] = organization_id

        return json.dumps({
            "invoice_id": invoice_id,
            **invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_invoice_payment",
                "description": (
                    "Marks an invoice as paid, and allows setting invoice fields "
                    "like worker_id, amount, dates, status, currency, and organization_id."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "The invoice to update"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Payment ID associated with the invoice"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker associated with the invoice"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Total invoice amount"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Invoice issue timestamp (ISO 8601 format)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Invoice due timestamp (ISO 8601 format)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Invoice status (default is 'paid' if not supplied)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency of the invoice (e.g., USD, INR)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID associated with the invoice"
                        }
                    },
                    "required": ["invoice_id"]
                }
            }
        }
