
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateWorkerBankInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, bank_info: Dict[str, Any]) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        user_id = workers[worker_id]["user_id"]
        bank_accounts = data.setdefault("bank_accounts", {})

        updated = None
        for acct_id, acct in bank_accounts.items():
            if acct.get("user_id") == user_id:
                acct.update(bank_info)
                updated = acct
                break

        if not updated:
            raise ValueError("Bank account not found for user")

        return json.dumps({"worker_id": worker_id, "updated": updated})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_worker_bank_info",
                "description": "Updates the bank details for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker whose bank info will be updated"
                        },
                        "bank_info": {
                            "type": "object",
                            "description": "Bank info fields to update (e.g., account_number, currency)",
                            "properties": {
                                "account_number": {"type": "string"},
                                "currency": {"type": "string"},
                                "bank_name": {"type": "string"}
                            }
                        }
                    },
                    "required": ["worker_id", "bank_info"]
                }
            }
        }
