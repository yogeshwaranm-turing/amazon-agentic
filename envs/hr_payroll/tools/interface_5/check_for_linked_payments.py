from tau_bench.envs.tool import Tool
from typing import Any, Dict

class CheckForLinkedPayments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> bool:
        for payment in data["payments"].values():
            if payment.get("invoice_id") == invoice_id:
                return True
        return False

    @staticmethod
    def get_info():
        return {
            "name": "check_for_linked_payments",
            "description": "Checks if a payment is linked to a given invoice.",
            "parameters": {
                "invoice_id": "str"
            },
            "returns": "bool"
        }