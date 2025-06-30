from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class MarkInvoiceReconciled(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> str:
        invoice = data["invoices"].get(invoice_id)
        if not invoice:
            raise ValueError("Invoice not found.")
        invoice["status"] = "reconciled"
        invoice["reconciled_at"] = datetime.utcnow().isoformat()
        return invoice_id

    @staticmethod
    def get_info():
        return {
            "name": "mark_invoice_reconciled",
            "description": "Marks an invoice as reconciled.",
            "parameters": {
                "invoice_id": "str"
            },
            "returns": "str"
        }