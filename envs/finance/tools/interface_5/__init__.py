
from .create_asset import CreateAsset
from .dispose_asset import DisposeAsset
from .get_audit_trails import GetAuditTrails
from .get_customer_details import GetCustomerDetails
from .get_depreciation_schedule import GetDepreciationSchedule
from .get_disposal_summary import GetDisposalSummary
from .list_assets_by_category import ListAssetsByCategory
from .list_assets_by_vendor import ListAssetsByVendor
from .list_assets import ListAssets
from .list_audit_trails_by_entity import ListAuditTrailsByEntity
from .transfer_to_human_agents import TransferToHumanAgents
from .update_asset_details import UpdateAssetDetails



ALL_TOOLS_INTERFACE_5 = [
    CreateAsset,
    DisposeAsset,
    GetAuditTrails,
    GetCustomerDetails,
    GetDepreciationSchedule,
    GetDisposalSummary,
    ListAssetsByCategory,
    ListAssetsByVendor,
    ListAssets,
    ListAuditTrailsByEntity,
    TransferToHumanAgents,
    UpdateAssetDetails,
]
