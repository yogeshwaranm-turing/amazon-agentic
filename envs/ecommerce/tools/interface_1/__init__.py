from tau_bench.envs.ecommerce.tools.interface_1.create_new_user import CreateNewUser
from tau_bench.envs.ecommerce.tools.interface_1.think import Think
from tau_bench.envs.ecommerce.tools.interface_1.create_new_product import CreateNewProduct
from tau_bench.envs.ecommerce.tools.interface_1.create_new_supplier import CreateNewSupplier
from tau_bench.envs.ecommerce.tools.interface_1.get_all_orders_related_to_user import GetAllOrdersRelatedToUser
from tau_bench.envs.ecommerce.tools.interface_1.get_order_information_by_id import GetOrderInformationById
from tau_bench.envs.ecommerce.tools.interface_1.get_product_information import GetProductInformation
from tau_bench.envs.ecommerce.tools.interface_1.get_user_info import GetUserInfo
from tau_bench.envs.ecommerce.tools.interface_1.import_purchase_order import ImportPurchaseOrder
from tau_bench.envs.ecommerce.tools.interface_1.place_order import PlaceOrder
from tau_bench.envs.ecommerce.tools.interface_1.update_order_status import UpdateOrderStatus
from tau_bench.envs.ecommerce.tools.interface_1.get_product_by_name import GetProductByName
from tau_bench.envs.ecommerce.tools.interface_1.get_product_by_supplier import GetProductBySupplier
from tau_bench.envs.ecommerce.tools.interface_1.get_supplier_by_zip_code import GetSupplierByZipCode

ALL_TOOLS_INTERFACE_1 = [
    CreateNewUser,
    Think,
    CreateNewProduct,
    CreateNewSupplier,
    GetAllOrdersRelatedToUser,
    GetOrderInformationById,
    GetProductInformation,
    GetUserInfo,
    ImportPurchaseOrder,
    PlaceOrder,
    UpdateOrderStatus,
    GetProductByName,
    GetProductBySupplier,
    GetSupplierByZipCode
]
