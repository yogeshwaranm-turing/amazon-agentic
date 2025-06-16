import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListInvoices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str, 
        status: str = None
    ) -> str:
        invs = data.get("invoices", {}).values()
        
        if not isinstance(invs, List):
            raise ValueError("Invoice data is not in the expected format.")
        
        results = [i for i in invs if i.get("user_id") == user_id]
        
        if status:
            results = [i for i in results if i.get("status") == status]
            
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_invoices",
                "description": "Retrieve invoices for a customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string"
                        },
                        "status": {
                            "type": "string"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }