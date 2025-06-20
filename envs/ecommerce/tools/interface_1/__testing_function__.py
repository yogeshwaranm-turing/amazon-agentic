import os
import json
from tau_bench.envs.ecommerce.tools.interface_1.place_order import PlaceOrder
from tau_bench.envs.ecommerce.tools.interface_1.create_new_product import CreateNewProduct  # added import
from tau_bench.envs.ecommerce.tools.interface_1.create_new_supplier import CreateNewSupplier  # new import
from tau_bench.envs.ecommerce.tools.interface_1.import_purchase_order import ImportPurchaseOrder
from tau_bench.envs.ecommerce.tools.interface_1.create_new_user import CreateNewUser  # new import
from tau_bench.envs.ecommerce.tools.interface_1.get_user_info import GetUserInfo  # new import
from tau_bench.envs.ecommerce.tools.interface_1.update_order_status import UpdateOrderStatus  # new import
from tau_bench.envs.ecommerce.tools.interface_1.get_order_information_by_id import GetOrderInformationById  # new import
from tau_bench.envs.ecommerce.tools.interface_1.get_all_orders_related_to_user import GetAllOrdersRelatedToUser
from tau_bench.envs.ecommerce.tools.interface_1.get_product_information import GetProductInformation  # new import
from tau_bench.envs.ecommerce.tools.interface_1.get_product_by_name import GetProductByName  # new import
from tau_bench.envs.ecommerce.tools.interface_1.get_product_by_supplier import GetProductBySupplier  # new import
# Add a dynamic base directory for JSON files
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def test_place_order():
    # Load users and products data from JSON files
    with open(os.path.join(BASE_DATA_DIR, "users.json"), "r") as f:
        users = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    # New: load sales_orders.json
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    # New: load sales_order_items.json
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)

    # Set up the data dictionary with sales_orders and sales_order_items loaded from JSON
    data = {
        "users": users,
        "products": products,
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items
    }

    # Use an existing user id from users.json, e.g. "USR001"
    user_id = "USR001"
    order_date = "2024-06-01"
    items = [
        {
            "product_id": "PRD0001",
            "quantity": 2,
            "unit_price": 10.0
        }
    ]

    result = PlaceOrder.invoke(data, user_id, order_date, items)
    print("Order Result:", result)

def test_create_new_product():
    # Load products and suppliers data
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)

    data = {
        "products": products,
        "suppliers": suppliers
    }

    # Test creating a new product with unique product_id
    result = CreateNewProduct.invoke(data, "PRD0021", "New Product", "Description for new product", "SUP001", 99.99)
    print("Create Product Result:", result)

def test_create_new_supplier():
    # Load suppliers data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    data = {
        "suppliers": suppliers
    }
    # Test creating a new supplier with unique supplier_id
    result = CreateNewSupplier.invoke(
        data,
        supplier_id="SUP011",
        name="Supplier 11",
        contact_email="supplier11@example.com",
        address="111 Supplier St",
        city="City11",
        state="ST11",
        zip_code="11111",
        country="USA"
    )
    print("Create Supplier Result:", result)

def test_import_purchase_order():
    # Load suppliers, products, and purchase_orders data
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "purchase_orders.json"), "r") as f:
        purchase_orders = json.load(f)
    # New: load purchase_order_items.json
    with open(os.path.join(BASE_DATA_DIR, "purchase_order_items.json"), "r") as f:
        purchase_order_items = json.load(f)

    # Set purchase_order_items as empty dict for testing
    data = {
        "suppliers": suppliers,
        "products": products,
        "purchase_orders": purchase_orders,
        "purchase_order_items": purchase_order_items
    }

    supplier_id = "SUP001"
    order_date = "2024-07-01"
    items = [
        {
            "product_id": "PRD0001",
            "quantity": 3,
            "unit_cost": 50.0
        }
    ]
    result = ImportPurchaseOrder.invoke(data, supplier_id, order_date, items)
    print("Import Purchase Order Result:", result)

def test_create_new_user():
    # Load users data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "users.json"), "r") as f:
        users = json.load(f)
    data = {"users": users}
    # Test creating a new user with valid data
    result = CreateNewUser.invoke(
        data,
        first_name="Sam",
        last_name="Doe",
        email="sam.doe@example.com",
        address="123 New St",
        city="NewCity",
        state="NC",
        zip_code="12345",
        country="USA"
    )
    print("Create New User Result:", result)

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

def test_update_order_status():
    import json
    # Load sales_orders and sales_order_items JSON
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items
    }
    # Update order "SO0001" to status "Confirmed"
    result = UpdateOrderStatus.invoke(data, "SO0001", "Confirmed")
    print("Update Order Status Result:", result)

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

def test_get_all_orders_related_to_user():
    import json
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_order_items.json"), "r") as f:
        sales_order_items = json.load(f)
    data = {
        "sales_orders": sales_orders,
        "sales_order_items": sales_order_items
    }
    user_id = "USR001"
    result = GetAllOrdersRelatedToUser.invoke(data, user_id)
    print(f"Orders related to {user_id}:", result)

def test_get_product_information():
    import json
    # Load products data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    data = {"products": products}
    # Test valid product_id
    result_valid = GetProductInformation.invoke(data, "PRD0001")
    print("Get Product Info for PRD0001:", result_valid)
    # Test invalid product_id
    result_invalid = GetProductInformation.invoke(data, "INVALID_ID")
    print("Get Product Info for INVALID_ID:", result_invalid)

def test_get_product_by_name():
    import json
    import os
    # Load products data
    BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    data = {"products": products}
    # Test with a valid product name (adjust "ValidProductName" as needed)
    result_valid = GetProductByName.invoke(data, "Eco-Friendly Reusable Water Bottle")
    print("Get Product By Name (valid):", result_valid)
    # Test with an invalid product name
    result_invalid = GetProductByName.invoke(data, "NonExistentProduct")
    print("Get Product By Name (invalid):", result_invalid)

def test_get_product_by_supplier():
    import json
    # Load products data from JSON file
    with open(os.path.join(BASE_DATA_DIR, "products.json"), "r") as f:
        products = json.load(f)
    data = {"products": products}
    # Test with a valid supplier id (adjust "SUP001" as needed)
    result_valid = GetProductBySupplier.invoke(data, "SUP001")
    print("Get Product By Supplier (valid):", result_valid)
    # Test with an invalid supplier id
    result_invalid = GetProductBySupplier.invoke(data, "INVALID_SUP")
    print("Get Product By Supplier (invalid):", result_invalid)

def test_get_supplier_by_zip_code():
    import os, json
    from tau_bench.envs.ecommerce.tools.interface_1.get_supplier_by_zip_code import GetSupplierByZipCode
    BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    with open(os.path.join(BASE_DATA_DIR, "suppliers.json"), "r") as f:
        suppliers = json.load(f)
    data = {"suppliers": suppliers}
    # Adjust "12345" to a zip code that exists in your test data
    result_valid = GetSupplierByZipCode.invoke(data, "62704")
    print("Get Supplier By Zip Code (valid):", result_valid)
    result_invalid = GetSupplierByZipCode.invoke(data, "00000")
    print("Get Supplier By Zip Code (invalid):", result_invalid)

if __name__ == "__main__":
    test_place_order()
    test_create_new_product()
    test_create_new_supplier()
    test_import_purchase_order()
    test_create_new_user()
    test_get_user_info()
    test_update_order_status()
    test_get_order_information_by_id()
    test_get_all_orders_related_to_user()
    test_get_product_information()
    test_get_product_by_name()
    test_get_product_by_supplier()  # new test function call
    test_get_supplier_by_zip_code()

