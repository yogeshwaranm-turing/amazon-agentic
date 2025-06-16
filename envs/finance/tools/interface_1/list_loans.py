import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListLoans(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str
    ) -> str:
        loans = data.get("loans", {})
        # result = [l for l in loans if isinstance(l, dict) and l.get("user_id") == user_id]
        result = {lid: loan for lid, loan in loans.items() if loan.get("user_id") == user_id}
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_loans",
                "description": "Fetch all loans for a customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }