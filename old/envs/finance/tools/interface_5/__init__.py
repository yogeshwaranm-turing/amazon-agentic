from .approve_disposal import ApproveDisposal
from .assign_asset_to_user import AssignAssetToUser
from .calculate_next_depreciation import CalculateNextDepreciation
from .create_asset import CreateAsset
from .delete_asset import DeleteAsset
from .delete_depreciation_entry import DeleteDepreciationEntry
from .delete_disposal import DeleteDisposal
from .dispose_asset import DisposeAsset
from .get_audit_trails import GetAuditTrails
from .get_customer_details import GetCustomerDetails
from .get_depreciation_schedule import GetDepreciationSchedule
from .get_disposal_summary import GetDisposalSummary
from .list_assets import ListAssets
from .list_assets_by_category import ListAssetsByCategory
from .list_assets_by_vendor import ListAssetsByVendor
from .list_audit_trails_by_entity import ListAuditTrailsByEntity
from .record_depreciation_entry import RecordDepreciationEntry
from .transfer_asset import TransferAsset
from .transfer_to_human_agents import TransferToHumanAgents
from .update_asset_details import UpdateAssetDetails
from .update_depreciation_entry import UpdateDepreciationEntry



ALL_TOOLS_INTERFACE_5 = [
    ApproveDisposal,
    AssignAssetToUser,
    CalculateNextDepreciation,
    CreateAsset,
    DeleteAsset,
    DeleteDepreciationEntry,
    DeleteDisposal,
    DisposeAsset,
    GetAuditTrails,
    GetCustomerDetails,
    GetDepreciationSchedule,
    GetDisposalSummary,
    ListAssets,
    ListAssetsByCategory,
    ListAssetsByVendor,
    ListAuditTrailsByEntity,
    RecordDepreciationEntry,
    TransferAsset,
    TransferToHumanAgents,
    UpdateAssetDetails,
    UpdateDepreciationEntry,
]
