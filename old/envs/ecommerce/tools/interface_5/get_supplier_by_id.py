import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSupplierById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], supplier_id: str) -> str:
        suppliers = data.get("suppliers", {})
        if supplier_id not in suppliers:
            return json.dumps({"error": "supplier_id not found"})
        supplier = suppliers[supplier_id]
        return json.dumps(supplier)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_supplier_by_id",
                "description": "Retrieve supplier information for the given supplier_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "Unique identifier for the supplier."
                        }
                    },
                    "required": ["supplier_id"]
                }
            }
        }
