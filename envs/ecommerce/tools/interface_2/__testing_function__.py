import os
import json
from tau_bench.envs.ecommerce.tools.interface_2.get_user_info import GetUserInfo  # new import
from tau_bench.envs.ecommerce.tools.interface_2.get_order_information_by_id import GetOrderInformationById  # new import
from tau_bench.envs.ecommerce.tools.interface_2.cancel_order import CancelOrder  # new import
from tau_bench.envs.ecommerce.tools.interface_2.list_purchase_order_by_supplier import ListPurchaseOrderBySupplier  # new import
from tau_bench.envs.ecommerce.tools.interface_2.get_supplier_info_by_id import GetSupplierInfoById  # new import
from tau_bench.envs.ecommerce.tools.interface_2.modify_sales_order_item import ModifySalesOrderItem
from tau_bench.envs.ecommerce.tools.interface_2.remove_sales_order_item import RemoveSalesOrderItem  # new import
from tau_bench.envs.ecommerce.tools.interface_2.add_new_sales_order_item import AddNewSalesOrderItem
from tau_bench.envs.ecommerce.tools.interface_2.modify_user_address import ModifyUserAddress

# Add a dynamic base directory for JSON files
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def test_get_user_info():
    with open(os.path.join(BASE_DATA_DIR, "users.json"), "r") as f:
        users = json.load(f)
    data = {"users": users}
    # Verify lookup by user_id
    result_id = GetUserInfo.invoke(data, "USR001")
    print("Get User Info by ID:", result_id)
    # Verify lookup by email
    result_email = GetUserInfo.invoke(data, "jordan.johnson002@example.com")
    print("Get User Info by Email:", result_email)
    # Verify not found
    result_email = GetUserInfo.invoke(data, "abc@example.com")
    print("Get User Info by Email:", result_email)

def test_get_order_information_by_id():
    # Load sales_orders and sales_order_items data from JSON files
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items
    }
    # Test valid order_id
    result_valid = GetOrderInformationById.invoke(data, "SO0001")
    print("Get Order Info for SO0001:", result_valid)
    # Test invalid order_id
    result_invalid = GetOrderInformationById.invoke(data, "INVALID_ID")
    print("Get Order Info for INVALID_ID:", result_invalid)

def test_cancel_order():
    # Load sales_orders data
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    data = {"sales_orders": sales_orders}
    # Provide an order id that exists and is Pending
    sales_order_id = "SO0002"
    reason = "Cancelled via test"
    result = CancelOrder.invoke(data, sales_order_id, reason)
    print("Cancel Order Result:", result)

def test_list_purchase_order_by_supplier():
    # Load purchase_orders data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "purchase_orders.json"), "r") as f:
        purchase_orders = json.load(f)
    data = {"purchase_orders": purchase_orders}
    supplier_id = "SUP001"  # example supplier id
    result = ListPurchaseOrderBySupplier.invoke(data, supplier_id)
    print("List Purchase Orders by Supplier Result:", result)

def test_get_supplier_info_by_id():
    import json
    # Load suppliers data
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    data = {"suppliers": suppliers}

    # Test valid supplier id
    result_valid = GetSupplierInfoById.invoke(data, "SUP001")
    print("Get Supplier Info for SUP001:", result_valid)

    # Test invalid supplier id
    result_invalid = GetSupplierInfoById.invoke(data, "INVALID_ID")
    print("Get Supplier Info for INVALID_ID:", result_invalid)

def test_modify_sales_order_item():
    # Load sales_order_items data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {"sales_order_items": sales_order_items}

    # Test modifying a sales order item; use sample sales_order_id and product_id
    sales_order_id = "SO0001"
    product_id = "PRD0001"
    new_quantity = 6 # New quantity must be > 0 and different from current quantity
    result = ModifySalesOrderItem.invoke(data, sales_order_id, product_id, new_quantity)
    print("Modify Sales Order Item Result:", result)

def test_remove_sales_order_item():
    # Load sales_orders and sales_order_items JSON data
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items
    }
    # Choose a sample sales_order_id and product_id to remove; adjust as needed for your data.
    sales_order_id = "SO0754"
    product_id = "PRD1733"
    result = RemoveSalesOrderItem.invoke(data, sales_order_id, product_id)
    print("Remove Sales Order Item Result:", result)

def test_add_new_sales_order_item():
    # Load sales_order_items data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {"sales_order_items": sales_order_items}
    order_id = "SO0003"  # sample order id
    product_id = "PRD0002"  # sample product id
    quantity = 4  # valid quantity (> 0)
    result = AddNewSalesOrderItem.invoke(data, order_id, product_id, quantity)
    print("Add New Sales Order Item Result:", result)

def test_calculate_total_cost_of_order():
    from tau_bench.envs.ecommerce.tools.interface_2.calculate_total_cost_of_order_by_id import CalculateTotalCostOfOrderById
    import json
    # Load sales_order_items and products data
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    data = {
        "sales_order_items": sales_order_items,
        "products": products
    }
    order_id = "SO0001"  # sample order id
    result = CalculateTotalCostOfOrderById.invoke(data, order_id)
    print("Calculate Total Cost Result:", result)

def test_modify_user_address():
    # Load users data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "users.json"), "r") as f:
        users = json.load(f)
    data = {"users": users}
    user_id = "USR001"  # existing user id
    new_address = "456 Updated Ave"
    result = ModifyUserAddress.invoke(data, user_id, new_address)
    print("Modify User Address Result:", result)

if __name__ == "__main__":
    test_get_user_info()
    test_get_order_information_by_id()
    test_cancel_order()  # new test
    test_list_purchase_order_by_supplier()  # new test function
    test_get_supplier_info_by_id()  # new test function
    test_modify_sales_order_item()  # new test function
    test_remove_sales_order_item()  # new test function already present
    test_add_new_sales_order_item()  # new test function added
    test_calculate_total_cost_of_order()  # new test function added
    test_modify_user_address()  # new test function added
