# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    with open(os.path.join(FOLDER_PATH, "suppliers.json")) as f:
        suppliers_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "products.json")) as f:
        products_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "purchase_orders.json")) as f:
        purchase_orders_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "purchase_order_items.json")) as f:
        purchase_order_items_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "users.json")) as f:
        users_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "sales_orders.json")) as f:
        sales_orders_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "sales_order_items.json")) as f:
        sales_order_items_data = json.load(f)
    with open(os.path.join(FOLDER_PATH, "shipping.json")) as f:
        shipping = json.load(f)
    return {
        "suppliers": suppliers_data,
        "products": products_data,
        "purchase_orders": purchase_orders_data,
        "purchase_order_items": purchase_order_items_data,
        "users": users_data,
        "sales_orders": sales_orders_data,
        "sales_order_items": sales_order_items_data,
        "shipping": shipping
    }
