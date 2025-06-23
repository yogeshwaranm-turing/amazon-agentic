import os
import json
from tau_bench.envs.ecommerce.tools.interface_4.change_shipment_status import ChangeShipmentStatus
from tau_bench.envs.ecommerce.tools.interface_4.confirm_payment import ConfirmPayment
from tau_bench.envs.ecommerce.tools.interface_4.confirm_shipment_for_order import ConfirmShipmentForOrder
from tau_bench.envs.ecommerce.tools.interface_4.delivery_shipment import DeliveryShipment
from tau_bench.envs.ecommerce.tools.interface_4.get_shipment_information_by_order_id import GetShipmentInformationByOrderId
from tau_bench.envs.ecommerce.tools.interface_4.get_shipment_information_by_tracking_number import GetShipmentInformationByTrackingNumber
from tau_bench.envs.ecommerce.tools.interface_4.modify_payment_method import ModifyPaymentMethod
from tau_bench.envs.ecommerce.tools.interface_4.modify_shipment_method import ModifyShipmentMethod

# Update dynamic base directory for JSON files - go three directories up to reference the 'data' folder
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def test_change_shipment_status():
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    data = {"shipping": shipping}
    tracking_number = "TRK948665"  # sample tracking number from shipping.json
    new_status = "Delivered"      # allowed status: "Preparing", "In Transit", "Delivered"
    result = ChangeShipmentStatus.invoke(data, tracking_number, new_status)
    print("Change Shipment Status Result:", result)

def test_confirm_payment():
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    data = {"sales_orders": sales_orders}
    sales_order_id = "SO0002"  # sample sales order id from sales_orders.json
    result = ConfirmPayment.invoke(data, sales_order_id)
    print("Confirm Payment Result:", result)

def test_confirm_shipment_for_order():
    # Fix: load sales_orders.json and pass data to ConfirmShipmentForOrder.invoke
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    data = {"sales_orders": sales_orders}
    order_id = "SO0001"
    result = ConfirmShipmentForOrder.invoke(data, order_id)
    print("Confirm Shipment For Order Result:", result)

def test_delivery_shipment():
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    data = {"shipping": shipping, "sales_orders": sales_orders}
    tracking_number = "TRK302527"  # sample tracking number from shipping.json
    result = DeliveryShipment.invoke(data, tracking_number)
    print("Delivery Shipment Result:", result)

def test_get_shipment_information_by_order_id():
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    data = {"shipping": shipping}
    order_id = "SO0902"  # sample sales order id expected in shipping.json
    result = GetShipmentInformationByOrderId.invoke(data, order_id)
    print("Get Shipment Information By Order ID Result:", result)

def test_get_shipment_information_by_tracking_number():
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    data = {"shipping": shipping}
    tracking_number = "TRK302527"  # sample tracking number from shipping.json
    result = GetShipmentInformationByTrackingNumber.invoke(data, tracking_number)
    print("Get Shipment Information By Tracking Number Result:", result)

def test_modify_payment_method():
    with open(os.path.join(BASE_DATA_DIR, "sales_orders.json"), "r") as f:
        sales_orders = json.load(f)
    data = {"sales_orders": sales_orders}
    sales_order_id = "SO0001"  # sample sales order id from sales_orders.json
    new_payment_method = "PayPal"  # assuming current payment method is not PayPal
    result = ModifyPaymentMethod.invoke(data, sales_order_id, new_payment_method)
    print("Modify Payment Method Result:", result)

def test_modify_shipment_method():
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    data = {"shipping": shipping}
    identifier = "TRK948665"  # sample tracking number from shipping.json
    new_shipment_method = "Standard"   # allowed values: "Standard", "Express"
    result = ModifyShipmentMethod.invoke(data, identifier, new_shipment_method)
    print("Modify Shipment Method Result:", result)

def test_update_shipping_address():
    from tau_bench.envs.ecommerce.tools.interface_4.update_shipping_address import UpdateShippingAddress
    with open(os.path.join(BASE_DATA_DIR, "shipping.json"), "r") as f:
        shipping = json.load(f)
    data = {"shipping": shipping}
    identifier = "TRK948665"  # sample tracking number from shipping.json
    new_address = "123 New Street, City, Country"
    result = UpdateShippingAddress.invoke(data, identifier, new_address)
    print("Update Shipping Address Result:", result)

if __name__ == "__main__":
    test_change_shipment_status()           # added test function for change shipment status
    test_confirm_payment()                  # added test function for confirm_payment
    test_confirm_shipment_for_order()       # added test function for confirm_shipment_for_order
    test_delivery_shipment()                # added test function for delivery_shipment
    test_get_shipment_information_by_order_id()  # added test function for get_shipment_information_by_order_id
    test_get_shipment_information_by_tracking_number()  # added test for get_shipment_information_by_tracking_number
    test_modify_payment_method()            # added test for modify payment method
    test_modify_shipment_method()           # added test for modify shipment method
    test_update_shipping_address()            # new test call for update_shipping_address

