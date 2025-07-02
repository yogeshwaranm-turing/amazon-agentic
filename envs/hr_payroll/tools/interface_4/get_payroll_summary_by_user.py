
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPayrollSummaryByUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        items = data.get("payroll_items", {})
        total_paid = sum(
            item.get("amount", 0)
            for item in items.values()
            if item.get("user_id") == user_id and item.get("status") == "paid"
        )
        return json.dumps({"user_id": user_id, "total_paid": round(total_paid, 2)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payroll_summary_by_user",
                "description": "Summarizes total payroll paid to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose payroll totals are being summarized"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
