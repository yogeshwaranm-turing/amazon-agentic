import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteProductById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str) -> str:
        # Verify products data exists and product_id exists in it
        if "products" not in data:
            return json.dumps({"error": "products data not provided"})
        if product_id not in data["products"]:
            return json.dumps({"error": f"Product '{product_id}' not found"})

        # Delete the product
        deleted_product = data["products"].pop(product_id)
        
        # Process purchase_order_items deletion
        deleted_purchase_order_items = []
        if "purchase_order_items" in data:
            poi_data = data["purchase_order_items"]
            if isinstance(poi_data, list):
                data["purchase_order_items"] = [
                    item for item in poi_data 
                    if (item.get("product_id") if isinstance(item, dict) else item) != product_id
                ]
                deleted_purchase_order_items = [
                    item for item in poi_data 
                    if (item.get("product_id") if isinstance(item, dict) else item) == product_id
                ]
            elif isinstance(poi_data, dict):
                new_poi = {}
                for key, value in poi_data.items():
                    if value.get("product_id") == product_id:
                        deleted_purchase_order_items.append(value)
                    else:
                        new_poi[key] = value
                data["purchase_order_items"] = new_poi
        
        # Process sales_order_items deletion
        deleted_sales_order_items = []
        if "sales_order_items" in data:
            soi_data = data["sales_order_items"]
            if isinstance(soi_data, list):
                data["sales_order_items"] = [
                    item for item in soi_data 
                    if (item.get("product_id") if isinstance(item, dict) else item) != product_id
                ]
                deleted_sales_order_items = [
                    item for item in soi_data 
                    if (item.get("product_id") if isinstance(item, dict) else item) == product_id
                ]
            elif isinstance(soi_data, dict):
                new_soi = {}
                for key, value in soi_data.items():
                    if value.get("product_id") == product_id:
                        deleted_sales_order_items.append(value)
                    else:
                        new_soi[key] = value
                data["sales_order_items"] = new_soi

        return json.dumps({
            "success": True,
            "deleted_product_id": product_id,
            "deleted_product": deleted_product,
            "deleted_purchase_order_items": deleted_purchase_order_items,
            "deleted_sales_order_items": deleted_sales_order_items
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_product_by_id",
                "description": "Delete product by product_id, after validating the existence, and remove its associations in purchase_order_items and sales_order_items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The ID of the product to be deleted."
                        }
                    },
                    "required": ["product_id"]
                }
            }
        }
