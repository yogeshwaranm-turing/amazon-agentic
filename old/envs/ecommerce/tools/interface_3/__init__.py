from tau_bench.envs.ecommerce.tools.interface_3.add_new_purchase_order_item import AddNewPurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.calculate_total_cost_of_purchase_order_by_id import CalculateTotalCostOfPurchaseOrderById
from tau_bench.envs.ecommerce.tools.interface_3.cancel_purchase_order_status import CancelPurchaseOrderStatus
from tau_bench.envs.ecommerce.tools.interface_3.get_purchase_order_information_by_id import GetPurchaseOrderInformationById
from tau_bench.envs.ecommerce.tools.interface_3.get_supplier_by_id import GetSupplierById
from tau_bench.envs.ecommerce.tools.interface_3.modify_quantity_of_purchase_order_item import ModifyQuantityOfPurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.modify_unit_cost_of_purchase_order_item import ModifyUnitCostOfPurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.remove_purchase_order_item import RemovePurchaseOrderItem
from tau_bench.envs.ecommerce.tools.interface_3.update_purchase_order_status import UpdatePurchaseOrderStatus
from tau_bench.envs.ecommerce.tools.interface_3.get_product_by_name import GetProductByName
from tau_bench.envs.ecommerce.tools.interface_3.get_product_by_supplier import GetProductBySupplier
from tau_bench.envs.ecommerce.tools.interface_3.get_supplier_by_zip_code import GetSupplierByZipCode
from tau_bench.envs.ecommerce.tools.interface_3.list_purchase_order_by_supplier import ListPurchaseOrderBySupplier
from tau_bench.envs.ecommerce.tools.interface_3.think import Think
from tau_bench.envs.ecommerce.tools.interface_3.get_user_info import GetUserInfo

ALL_TOOLS_INTERFACE_3 = [
    AddNewPurchaseOrderItem,
    CalculateTotalCostOfPurchaseOrderById,
    CancelPurchaseOrderStatus,
    GetPurchaseOrderInformationById,
    GetSupplierById,
    ModifyQuantityOfPurchaseOrderItem,
    ModifyUnitCostOfPurchaseOrderItem,
    RemovePurchaseOrderItem,
    UpdatePurchaseOrderStatus,
    GetProductByName,
    GetProductBySupplier,
    GetSupplierByZipCode,
    ListPurchaseOrderBySupplier,
    Think,
    GetUserInfo
]
