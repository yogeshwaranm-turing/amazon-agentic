import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifyPaymentMethod(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], sales_order_id: str, new_payment_method: str) -> str:
        # Allowed payment methods
        allowed_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
        if new_payment_method not in allowed_methods:
            return f"Error: payment_method must be one of {allowed_methods}"
        # Retrieve sales order data from data variable
        sales_orders = data.get("sales_orders", {})
        sales_order = sales_orders.get(sales_order_id)
        if sales_order is None:
            return f"Error: sales_order_id {sales_order_id} not found"
        current_method = sales_order.get("payment_method")
        if current_method == new_payment_method:
            return "Error: new payment method must be different from the current one"
        # Update payment method
        sales_order["payment_method"] = new_payment_method
        sales_orders[sales_order_id] = sales_order
        data["sales_orders"] = sales_orders
        return json.dumps(sales_order)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_payment_method",
                "description": ("Modify the payment method of a sales order. "
                                "Allowed payment methods: 'Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash'. "
                                "The new payment method must be different from the current one."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The identifier of the sales order."
                        },
                        "new_payment_method": {
                            "type": "string",
                            "description": "The new payment method."
                        }
                    },
                    "required": ["sales_order_id", "new_payment_method"]
                }
            }
        }
