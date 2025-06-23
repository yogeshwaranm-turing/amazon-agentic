import os
import json
from tau_bench.envs.ecommerce.tools.interface_5.change_supplier_for_purchase_order import ChangeSupplierForPurchaseOrder  # new import
from tau_bench.envs.ecommerce.tools.interface_5.delete_product_by_id import DeleteProductById  # new import
from tau_bench.envs.ecommerce.tools.interface_5.delete_purchase_order_by_id import DeletePurchaseOrderById  # new import
from tau_bench.envs.ecommerce.tools.interface_5.delete_sales_order_by_id import DeleteSalesOrderById  # new import
from tau_bench.envs.ecommerce.tools.interface_5.modify_supplier_address_city_state import ModifySupplierAddressCityState  # new import

BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def test_change_supplier_for_purchase_order():
    # Load purchase_orders and suppliers JSON data
    with open(os.path.join(BASE_DATA_DIR, "purchase_orders.json"), "r") as f:
        purchase_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    data = {
        "purchase_orders": purchase_orders,
        "suppliers": suppliers
    }
    purchase_order_id = "PO0001"  # sample purchase order id
    new_supplier_id = "SUP002"  # sample new supplier id
    result = ChangeSupplierForPurchaseOrder.invoke(data, purchase_order_id, new_supplier_id)
    print("Change Supplier for Purchase Order Result:", result)

def test_delete_product_by_id():
    # Load products JSON data
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    # Load purchase_order_items JSON data
    with open(os.path.join(BASE_DATA_DIR, "purchase_order_items.json"), "r") as f:
        purchase_order_items = json.load(f)
    # Load sales_order_items JSON data
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {
        "products": products,
        "purchase_order_items": purchase_order_items,
        "sales_order_items": sales_order_items,
        # ...existing optional data...
    }
    product_id = "PRD0010"  # sample product id
    result = DeleteProductById.invoke(data, product_id)
    print("Delete Product By Id Result:", result)

def test_delete_purchase_order_by_id():
    # Load purchase_orders and purchase_order_items JSON data
    purchase_orders = json.load(open(os.path.join(BASE_DATA_DIR, "purchase_orders.json"), "r"))
    purchase_order_items = json.load(open(os.path.join(BASE_DATA_DIR, "purchase_order_items.json"), "r"))
    data = {
        "purchase_orders": purchase_orders,
        "purchase_order_items": purchase_order_items
    }
    purchase_order_id = "PO0001"  # sample purchase order id
    result = DeletePurchaseOrderById.invoke(data, purchase_order_id)
    print("Delete Purchase Order By Id Result:", result)

def test_delete_sales_order_by_id():
    # Load sales_orders, sales_order_items and shipping_records JSON data
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping_records = json.load(f)
    data = {
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items,
        "shipping": shipping_records
    }
    sales_order_id = "SO0001"  # sample sales order id
    result = DeleteSalesOrderById.invoke(data, sales_order_id)
    print("Delete Sales Order By Id Result:", result)

def test_modify_supplier_address_city_state():
    # Load suppliers JSON data
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    data = {
        "suppliers": suppliers
    }
    supplier_id = "SUP001"  # sample supplier id
    new_address = "123 New Address"
    new_city = "New City"
    new_state = "New State"
    result = ModifySupplierAddressCityState.invoke(data, supplier_id, new_address, new_city, new_state)
    print("Modify Supplier Address, City, State Result:", result)

if __name__ == "__main__":
    test_change_supplier_for_purchase_order()
    test_delete_product_by_id()  # new test function called
    test_delete_purchase_order_by_id()  # new test function called
    test_delete_sales_order_by_id()  # new test function call
    test_modify_supplier_address_city_state()  # new test function call

