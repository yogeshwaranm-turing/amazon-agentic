import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateNewProduct(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_id: str,
        name: str,
        description: str,
        supplier_id: str,
        unit_price: float
    ) -> str:
        # Validate unique product_id
        if product_id in data["products"]:
            return "Error: product already exists"
        # Validate supplier_id exists in suppliers
        if supplier_id not in data["suppliers"]:
            return "Error: supplier not found"
        # Validate unit_price is greater than 0
        if unit_price <= 0:
            return "Error: unit price must be greater than 0"
        # Create new product entry
        product = {
            "product_id": product_id,
            "name": name,
            "description": description,
            "supplier_id": supplier_id,
            "unit_price": unit_price
        }
        data["products"][product_id] = product
        return json.dumps({"product": product})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        # Return metadata about the create_new_product function
        return {
            "type": "function",
            "function": {
                "name": "create_new_product",
                "description": "Create a new product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "Unique identifier for the product."
                        },
                        "name": {
                            "type": "string",
                            "description": "Name of the product."
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the product."
                        },
                        "supplier_id": {
                            "type": "string",
                            "description": "The ID of the supplier."
                        },
                        "unit_price": {
                            "type": "number",
                            "description": "The unit price of the product, must be greater than 0."
                        }
                    },
                    "required": ["product_id", "name", "description", "supplier_id", "unit_price"]
                }
            }
        }
