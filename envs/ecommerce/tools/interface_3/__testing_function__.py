import os
import json
from tau_bench.envs.ecommerce.tools.interface_3.add_new_purchase_order_item import AddNewPurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.calculate_total_cost_of_purchase_order_by_id import CalculateTotalCostOfPurchaseOrderById
from tau_bench.envs.ecommerce.tools.interface_3.cancel_purchase_order_status import CancelPurchaseOrderStatus  # new import
from tau_bench.envs.ecommerce.tools.interface_3.get_purchase_order_information_by_id import GetPurchaseOrderInformationById  # new import
from tau_bench.envs.ecommerce.tools.interface_3.get_supplier_by_id import GetSupplierById  # new import
from tau_bench.envs.ecommerce.tools.interface_3.modify_quantity_of_purchase_order_item import ModifyQuantityOfPurchaseOrderItem  # new import
from tau_bench.envs.ecommerce.tools.interface_3.modify_unit_cost_of_purchase_order_item import ModifyUnitCostOfPurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.remove_purchase_order_item import RemovePurchaseOrderItem  # new import
from tau_bench.envs.ecommerce.tools.interface_3.update_purchase_order_status import UpdatePurchaseOrderStatus  # new import

# Update dynamic base directory for JSON files - go three directories up to reference the 'data' folder
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def test_add_new_purchase_order_item_interface3():
    # Load data from JSON files
    purchase_orders_path = os.path.join(BASE_DATA_DIR, "purchase_orders.json")
    products_path = os.path.join(BASE_DATA_DIR, "products.json")
    poi_path = os.path.join(BASE_DATA_DIR, "purchase_order_items.json")
    with open(purchase_orders_path, "r") as f:
        purchase_orders = json.load(f)
    with open(products_path, "r") as f:
        products = json.load(f)
    if os.path.exists(poi_path):
        with open(poi_path, "r") as f:
            purchase_order_items = json.load(f)
    else:
        purchase_order_items = {}
    
    data = {
        "purchase_orders": purchase_orders,
        "products": products,
        "purchase_order_items": purchase_order_items
    }
    
    # Sample data (ensure purchase_order_id and product_id exist in the respective JSON files)
    purchase_order_id = "PO0002"
    product_id = "PRD0010"
    quantity = 10
    unit_cost = 15.99
    result = AddNewPurchaseOrderItem.invoke(data, purchase_order_id, product_id, quantity, unit_cost)
    print("Add New Purchase Order Item (Interface 3) Result:", result)

def test_calculate_total_cost_of_purchase_order_by_id():
    # Load data from JSON files
    purchase_orders_path = os.path.join(BASE_DATA_DIR, "purchase_orders.json")
    poi_path = os.path.join(BASE_DATA_DIR, "purchase_order_items.json")
    with open(purchase_orders_path, "r") as f:
        purchase_orders = json.load(f)
    if os.path.exists(poi_path):
        with open(poi_path, "r") as f:
            purchase_order_items = json.load(f)
    else:
        purchase_order_items = {}
    
    data = {
        "purchase_orders": purchase_orders,
        "purchase_order_items": purchase_order_items,
        # ...other data if needed...
    }
    
    # Specify a purchase_order_id present in your test JSON data
    purchase_order_id = "PO0002"
    result = CalculateTotalCostOfPurchaseOrderById.invoke(data, purchase_order_id)
    print("Calculate Total Cost Result:", result)

def test_cancel_purchase_order_status():
    # Load purchase_orders from JSON file
    purchase_orders_path = os.path.join(BASE_DATA_DIR, "purchase_orders.json")
    with open(purchase_orders_path, "r") as f:
        purchase_orders = json.load(f)
    
    data = {
        "purchase_orders": purchase_orders,
        # ...other data if needed...
    }
    
    purchase_order_id = "PO0003"  # ensure this ID exists in purchase_orders.json for testing
    result = CancelPurchaseOrderStatus.invoke(data, purchase_order_id)
    print("Cancel Purchase Order Status Result:", result)

def test_get_purchase_order_information_by_id():
    # Load purchase_orders from JSON file
    purchase_orders_path = os.path.join(BASE_DATA_DIR, "purchase_orders.json")
    with open(purchase_orders_path, "r") as f:
        purchase_orders = json.load(f)
    
    data = {
        "purchase_orders": purchase_orders
    }
    
    purchase_order_id = "PO0001"  # update id as needed for testing
    result = GetPurchaseOrderInformationById.invoke(data, purchase_order_id)
    print("Get Purchase Order Information Result:", result)

def test_get_supplier_by_id():
    # Load suppliers from JSON file
    suppliers_path = os.path.join(BASE_DATA_DIR, "suppliers.json")
    if os.path.exists(suppliers_path):
        with open(suppliers_path, "r") as f:
            suppliers = json.load(f)
    else:
        suppliers = {}
    
    data = {
        "suppliers": suppliers
    }
    
    supplier_id = "SUP001"  # update id as needed for testing
    result = GetSupplierById.invoke(data, supplier_id)
    print("Get Supplier By ID Result:", result)

def test_modify_quantity_of_purchase_order_item():
    # Load purchase_order_items from JSON file
    poi_path = os.path.join(BASE_DATA_DIR, "purchase_order_items.json")
    if os.path.exists(poi_path):
        with open(poi_path, "r") as f:
            purchase_order_items = json.load(f)
    else:
        purchase_order_items = {}
    
    data = {
        "purchase_order_items": purchase_order_items
    }
    
    purchase_order_id = "PO0001"   # update as needed based on test data
    product_id = "PRD0001"         # update as needed based on test data
    new_quantity = 20
    result = ModifyQuantityOfPurchaseOrderItem.invoke(data, purchase_order_id, product_id, new_quantity)
    print("Modify Quantity of Purchase Order Item Result:", result)

def test_modify_unit_cost_of_purchase_order_item():
    # Load purchase_order_items from JSON file
    poi_path = os.path.join(BASE_DATA_DIR, "purchase_order_items.json")
    if os.path.exists(poi_path):
        with open(poi_path, "r") as f:
            purchase_order_items = json.load(f)
    else:
        purchase_order_items = {}
    data = {
        "purchase_order_items": purchase_order_items
    }
    purchase_order_id = "PO0001"  # update as needed based on test data
    quantity = 5               # ensure this quantity exists in one of the items for PO0001
    new_unit_cost = 20.50      # new unit cost value for testing
    result = ModifyUnitCostOfPurchaseOrderItem.invoke(data, purchase_order_id, quantity, new_unit_cost)
    print("Modify Unit Cost of Purchase Order Item Result:", result)

def test_remove_purchase_order_item():
    # Load purchase_order_items from JSON file
    poi_path = os.path.join(BASE_DATA_DIR, "purchase_order_items.json")
    if os.path.exists(poi_path):
        with open(poi_path, "r") as f:
            purchase_order_items = json.load(f)
    else:
        purchase_order_items = {}
    data = {
        "purchase_order_items": purchase_order_items
    }
    purchase_order_id = "PO0001"  # update based on test data
    product_id = "PRD0001"       # update based on test data
    result = RemovePurchaseOrderItem.invoke(data, purchase_order_id, product_id)
    print("Remove Purchase Order Item Result:", result)

def test_update_purchase_order_status():
    # Load purchase_orders from JSON file
    purchase_orders_path = os.path.join(BASE_DATA_DIR, "purchase_orders.json")
    with open(purchase_orders_path, "r") as f:
        purchase_orders = json.load(f)
    data = {
        "purchase_orders": purchase_orders
    }
    purchase_order_id = "PO0001"  # update as needed for test data
    new_status = "Confirmed"      # allowed statuses: Pending, Confirmed, Delivered, Cancelled
    result = UpdatePurchaseOrderStatus.invoke(data, purchase_order_id, new_status)
    print("Update Purchase Order Status Result:", result)

if __name__ == "__main__":
    test_add_new_purchase_order_item_interface3()
    test_calculate_total_cost_of_purchase_order_by_id()
    test_cancel_purchase_order_status()
    test_get_purchase_order_information_by_id()
    test_get_supplier_by_id()
    test_modify_quantity_of_purchase_order_item()
    test_modify_unit_cost_of_purchase_order_item()
    test_remove_purchase_order_item()
    test_update_purchase_order_status()