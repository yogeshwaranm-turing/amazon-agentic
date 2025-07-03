import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSupplierInfoById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], supplier_id: str) -> str:
        """
        Retrieve supplier info by supplier_id.
        - Expects a 'suppliers' dictionary in data.
        - Returns supplier information as a JSON string.
        """
        suppliers = data.get("suppliers", {})
        if supplier_id not in suppliers:
            return json.dumps({"error": f"Supplier {supplier_id} not found"})
        return json.dumps(suppliers[supplier_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_supplier_info_by_id",
                "description": "Returns information for a supplier given its supplier_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The ID of the supplier."
                        }
                    },
                    "required": ["supplier_id"]
                }
            }
        }
