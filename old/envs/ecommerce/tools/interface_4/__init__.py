from tau_bench.envs.ecommerce.tools.interface_4.change_shipment_status import ChangeShipmentStatus
from tau_bench.envs.ecommerce.tools.interface_4.confirm_payment import ConfirmPayment
from tau_bench.envs.ecommerce.tools.interface_4.confirm_shipment_for_order import ConfirmShipmentForOrder
from tau_bench.envs.ecommerce.tools.interface_4.delivery_shipment import DeliveryShipment
from tau_bench.envs.ecommerce.tools.interface_4.get_user_info import GetUserInfo
from tau_bench.envs.ecommerce.tools.interface_4.get_all_orders_related_to_user import GetAllOrdersRelatedToUser
from tau_bench.envs.ecommerce.tools.interface_4.get_order_information_by_id import GetOrderInformationById
from tau_bench.envs.ecommerce.tools.interface_4.get_product_by_name import GetProductByName
from tau_bench.envs.ecommerce.tools.interface_4.get_product_by_supplier import GetProductBySupplier
from tau_bench.envs.ecommerce.tools.interface_4.get_shipment_information_by_order_id import GetShipmentInformationByOrderId
from tau_bench.envs.ecommerce.tools.interface_4.get_shipment_information_by_tracking_number import GetShipmentInformationByTrackingNumber
from tau_bench.envs.ecommerce.tools.interface_4.get_supplier_by_zip_code import GetSupplierByZipCode
from tau_bench.envs.ecommerce.tools.interface_4.modify_payment_method import ModifyPaymentMethod
from tau_bench.envs.ecommerce.tools.interface_4.modify_shipment_method import ModifyShipmentMethod
from tau_bench.envs.ecommerce.tools.interface_4.think import Think
from tau_bench.envs.ecommerce.tools.interface_4.update_shipping_address import UpdateShippingAddress


ALL_TOOLS_INTERFACE_4 = [
    ChangeShipmentStatus,
    ConfirmPayment,
    ConfirmShipmentForOrder,
    DeliveryShipment,
    GetUserInfo,
    GetAllOrdersRelatedToUser,
    GetOrderInformationById,
    GetProductByName,
    GetProductBySupplier,
    GetShipmentInformationByOrderId,
    GetShipmentInformationByTrackingNumber,
    GetSupplierByZipCode,
    ModifyPaymentMethod,
    ModifyShipmentMethod,
    Think,
    UpdateShippingAddress
]
