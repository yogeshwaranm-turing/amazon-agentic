
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitPayrollItemAdjustment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contract_id: str, amount: float, reason: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Invalid contract")

        worker_id = contracts[contract_id]["worker_id"]
        org_id = contracts[contract_id]["organization_id"]
        user_id = contracts[contract_id]["user_id"]

        item_id = str(uuid.uuid4())
        item = {
            "contract_id": contract_id,
            "worker_id": worker_id,
            "run_id": None,
            "amount": round(amount, 2),
            "currency": contracts[contract_id]["currency"],
            "status": "pending",
            "user_id": user_id,
            "note": reason
        }

        data.setdefault("payroll_items", {})[item_id] = item
        return json.dumps({"item_id": item_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_payroll_item_adjustment",
                "description": "Adds a bonus/deduction to a payroll item",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "ID of contract receiving adjustment"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount of adjustment"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for adjustment"
                        }
                    },
                    "required": ["contract_id", "amount", "reason"]
                }
            }
        }
