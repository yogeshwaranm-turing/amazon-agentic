import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeletePurchaseOrderById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str) -> str:
        # Validate purchase_orders exists
        if "purchase_orders" not in data:
            return json.dumps({"error": "purchase_orders data not provided"})
        if purchase_order_id not in data["purchase_orders"]:
            return json.dumps({"error": f"Purchase order '{purchase_order_id}' not found"})

        # Delete the purchase order
        deleted_purchase_order = data["purchase_orders"].pop(purchase_order_id)

        # Process deletion of related purchase_order_items
        deleted_purchase_order_items = []
        if "purchase_order_items" in data:
            poi_data = data["purchase_order_items"]
            if isinstance(poi_data, list):
                deleted_purchase_order_items = [
                    item for item in poi_data 
                    if (item.get("purchase_order_id") if isinstance(item, dict) else item) == purchase_order_id
                ]
                data["purchase_order_items"] = [
                    item for item in poi_data 
                    if (item.get("purchase_order_id") if isinstance(item, dict) else item) != purchase_order_id
                ]
            elif isinstance(poi_data, dict):
                new_poi = {}
                for key, value in poi_data.items():
                    if value.get("purchase_order_id") == purchase_order_id:
                        deleted_purchase_order_items.append(value)
                    else:
                        new_poi[key] = value
                data["purchase_order_items"] = new_poi

        return json.dumps({
            "success": True,
            "deleted_purchase_order_id": purchase_order_id,
            "deleted_purchase_order": deleted_purchase_order,
            "deleted_purchase_order_items": deleted_purchase_order_items
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_purchase_order_by_id",
                "description": "Delete a purchase order by purchase_order_id and remove all related purchase_order_items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The ID of the purchase order to be deleted."
                        }
                    },
                    "required": ["purchase_order_id"]
                }
            }
        }
