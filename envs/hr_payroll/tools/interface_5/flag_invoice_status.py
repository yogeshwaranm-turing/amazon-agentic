from tau_bench.envs.tool import Tool
from typing import Any, Dict

class FlagInvoiceStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, status: str = "overdue") -> str:
        invoice = data["invoices"].get(invoice_id)
        if not invoice:
            raise ValueError("Invoice not found.")
        invoice["status"] = status
        return invoice_id

    @staticmethod
    def get_info():
        return {
            "name": "flag_invoice_status",
            "description": "Flags an invoice with a specific status, typically 'overdue'.",
            "parameters": {
                "invoice_id": "str",
                "status": "str"
            },
            "returns": "str"
        }