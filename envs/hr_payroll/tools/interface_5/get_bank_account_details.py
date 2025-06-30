from typing import Dict, Any
from tau_bench.envs.tool import Tool

class GetBankAccountDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, bank_account_id: str) -> Dict[str, Any]:
        return {
            "bank_account_id": bank_account_id,
            "user_id": user_id,
            "provider_id": "BANK_WISE_UK",
            "currency": "GBP",
            "status": "active",
        }

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_bank_account_details",
                "description": "Retrieve details for a specific bank account belonging to a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "bank_account_id": {"type": "string"}
                    },
                    "required": ["user_id", "bank_account_id"]
                }
            }
        }