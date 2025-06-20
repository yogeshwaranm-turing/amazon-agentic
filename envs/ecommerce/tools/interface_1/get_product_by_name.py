import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetProductByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_name: str) -> str:
        products = data.get("products", {})
        # Iterate through products assuming products is a dict of product_id to product info.
        for product in products.values():
            if product.get("name") == product_name:
                return json.dumps(product)
        return f"Error: product with name {product_name} not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_product_by_name",
                "description": "Retrieve product information using product name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The name of the product."
                        }
                    },
                    "required": ["product_name"]
                }
            }
        }
