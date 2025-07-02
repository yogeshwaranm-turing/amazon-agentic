import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSupplierByZipCode(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], zip_code: str) -> str:
        suppliers = data.get("suppliers", {})
        result = [supplier for supplier in suppliers.values() if supplier.get("zip_code") == zip_code]
        if not result:
            return f"Error: no supplier found for zip code {zip_code}"
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_supplier_by_zip_code",
                "description": "Retrieve suppliers by zip code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "zip_code": {
                            "type": "string",
                            "description": "The zip code of the supplier."
                        }
                    },
                    "required": ["zip_code"]
                }
            }
        }

