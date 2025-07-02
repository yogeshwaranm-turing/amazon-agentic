import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ImportPurchaseOrder(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        supplier_id: str,
        order_date: str,
        items: List[Dict[str, Any]]
    ) -> str:
        # Check if supplier exists
        if supplier_id not in data.get("suppliers", {}):
            return "Error: supplier not found"
        
        # Generate purchase_order_id with format POXXXX
        po_keys = data.get("purchase_orders", {})
        if po_keys:
            max_po = max(int(key[2:]) for key in po_keys.keys())
            new_po_num = max_po + 1
        else:
            new_po_num = 1
        purchase_order_id = f"PO{str(new_po_num).zfill(4)}"
        
        # Create purchase order record
        purchase_order = {
            "purchase_order_id": purchase_order_id,
            "supplier_id": supplier_id,
            "order_date": order_date
        }
        data.setdefault("purchase_orders", {})[purchase_order_id] = purchase_order

        # Generate purchase_order_item ids with format POI00001
        poi_keys = data.get("purchase_order_items", {})
        if poi_keys:
            max_poi = max(int(key[3:]) for key in poi_keys.keys())
            counter = max_poi + 1
        else:
            counter = 1

        order_items = []
        for item in items:
            # Check if product exists in products.json
            product_id = item.get("product_id")
            if product_id not in data.get("products", {}):
                return f"Error: product {product_id} not found"
            # New check: Ensure quantity and unit_cost are greater than 0
            if item.get("quantity", 0) <= 0 or item.get("unit_cost", 0) <= 0:
                return f"Error: invalid quantity or unit_cost for product {product_id}"
            purchase_order_item_id = f"POI{str(counter).zfill(5)}"
            counter += 1
            order_item = {
                "po_item_id": purchase_order_item_id,
                "purchase_order_id": purchase_order_id,
                "product_id": product_id,
                "quantity": item["quantity"],
                "unit_cost": item["unit_cost"],
            }
            data.setdefault("purchase_order_items", {})[purchase_order_item_id] = order_item
            order_items.append(order_item)
        
        return json.dumps({"purchase_order": purchase_order, "order_items": order_items})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        # Return metadata for the import_purchase_order tool
        return {
            "type": "function",
            "function": {
                "name": "import_purchase_order",
                "description": "Import a purchase order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The supplier ID for the purchase order."
                        },
                        "order_date": {
                            "type": "string",
                            "description": "The date of the purchase order in format 'YYYY-MM-DD'."
                        },
                        "items": {
                            "type": "array",
                            "description": "An array of items in the purchase order.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "product_id": {
                                        "type": "string",
                                        "description": "The product ID to order."
                                    },
                                    "quantity": {
                                        "type": "number",
                                        "description": "The quantity to order."
                                    },
                                    "unit_cost": {
                                        "type": "number",
                                        "description": "The unit cost for the product."
                                    }
                                },
                                "required": ["product_id", "quantity", "unit_cost"]
                            }
                        }
                    },
                    "required": ["supplier_id", "order_date", "items"]
                }
            }
        }
