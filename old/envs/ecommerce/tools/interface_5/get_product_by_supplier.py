import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetProductBySupplier(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], supplier_id: str) -> str:
        products = data.get("products", {})
        result = [product for product in products.values() if product.get("supplier_id") == supplier_id]
        if not result:
            return f"Error: no products found for supplier {supplier_id}"
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_product_by_supplier",
                "description": "Retrieve products by supplier id.",
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
