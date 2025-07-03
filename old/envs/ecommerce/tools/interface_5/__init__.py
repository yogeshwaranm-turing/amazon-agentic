from tau_bench.envs.ecommerce.tools.interface_5.change_supplier_for_purchase_order import ChangeSupplierForPurchaseOrder
from tau_bench.envs.ecommerce.tools.interface_5.delete_product_by_id import DeleteProductById
from tau_bench.envs.ecommerce.tools.interface_5.delete_purchase_order_by_id import DeletePurchaseOrderById
from tau_bench.envs.ecommerce.tools.interface_5.delete_sales_order_by_id import DeleteSalesOrderById
from tau_bench.envs.ecommerce.tools.interface_5.get_all_orders_related_to_user import GetAllOrdersRelatedToUser
from tau_bench.envs.ecommerce.tools.interface_5.get_product_by_name import GetProductByName
from tau_bench.envs.ecommerce.tools.interface_5.get_product_by_supplier import GetProductBySupplier
from tau_bench.envs.ecommerce.tools.interface_5.get_purchase_order_information_by_id import GetPurchaseOrderInformationById
from tau_bench.envs.ecommerce.tools.interface_5.get_supplier_by_id import GetSupplierById
from tau_bench.envs.ecommerce.tools.interface_5.get_supplier_by_zip_code import GetSupplierByZipCode
from tau_bench.envs.ecommerce.tools.interface_5.get_user_info import GetUserInfo
from tau_bench.envs.ecommerce.tools.interface_5.list_purchase_order_by_supplier import ListPurchaseOrderBySupplier
from tau_bench.envs.ecommerce.tools.interface_5.modify_supplier_address_city_state import ModifySupplierAddressCityState
from tau_bench.envs.ecommerce.tools.interface_5.think import Think

ALL_TOOLS_INTERFACE_5 = [
    ChangeSupplierForPurchaseOrder,
    DeleteProductById,
    DeletePurchaseOrderById,
    DeleteSalesOrderById,
    GetAllOrdersRelatedToUser,
    GetProductByName,
    GetProductBySupplier,
    GetPurchaseOrderInformationById,
    GetSupplierById,
    GetSupplierByZipCode,
    GetUserInfo,
    ListPurchaseOrderBySupplier,
    ModifySupplierAddressCityState,
    Think
]
