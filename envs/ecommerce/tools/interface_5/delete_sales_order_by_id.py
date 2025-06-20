import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteSalesOrderById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], sales_order_id: str) -> str:
        # Validate sales_orders exists
        if "sales_orders" not in data:
            return json.dumps({"error": "sales_orders data not provided"})
        if sales_order_id not in data["sales_orders"]:
            return json.dumps({"error": f"Sales order '{sales_order_id}' not found"})
        
        # Delete the sales order
        deleted_sales_order = data["sales_orders"].pop(sales_order_id)

        # Process deletion of related sales_order_items
        deleted_sales_order_items = []
        if "sales_order_items" in data:
            soi_data = data["sales_order_items"]
            if isinstance(soi_data, list):
                deleted_sales_order_items = [
                    item for item in soi_data
                    if (item.get("sales_order_id") if isinstance(item, dict) else item) == sales_order_id
                ]
                data["sales_order_items"] = [
                    item for item in soi_data
                    if (item.get("sales_order_id") if isinstance(item, dict) else item) != sales_order_id
                ]
            elif isinstance(soi_data, dict):
                new_soi = {}
                for key, value in soi_data.items():
                    if value.get("sales_order_id") == sales_order_id:
                        deleted_sales_order_items.append(value)
                    else:
                        new_soi[key] = value
                data["sales_order_items"] = new_soi

        # Process deletion of related shipping records
        deleted_shipping_records = []
        if "shipping" in data:
            sr_data = data["shipping"]
            if isinstance(sr_data, list):
                deleted_shipping_records = [
                    record for record in sr_data
                    if (record.get("sales_order_id") if isinstance(record, dict) else record) == sales_order_id
                ]
                data["shipping"] = [
                    record for record in sr_data
                    if (record.get("sales_order_id") if isinstance(record, dict) else record) != sales_order_id
                ]
            elif isinstance(sr_data, dict):
                new_sr = {}
                for key, value in sr_data.items():
                    if value.get("sales_order_id") == sales_order_id:
                        deleted_shipping_records.append(value)
                    else:
                        new_sr[key] = value
                data["shipping"] = new_sr

        return json.dumps({
            "success": True,
            "deleted_sales_order_id": sales_order_id,
            "deleted_sales_order": deleted_sales_order,
            "deleted_sales_order_items": deleted_sales_order_items,
            "deleted_shipping_records": deleted_shipping_records
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_sales_order_by_id",
                "description": "Delete a sales order by sales_order_id along with its associated sales_order_items and shipping records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The ID of the sales order to be deleted."
                        }
                    },
                    "required": ["sales_order_id"]
                }
            }
        }
