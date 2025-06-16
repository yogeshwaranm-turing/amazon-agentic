import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetProductInformation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str) -> str:
        product = data.get("products", {}).get(product_id)
        if not product:
            return f"Error: product {product_id} not found"
        return json.dumps(product)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_product_information",
                "description": "Retrieve product information using product_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The ID of the product."
                        }
                    },
                    "required": ["product_id"]
                }
            }
        }
