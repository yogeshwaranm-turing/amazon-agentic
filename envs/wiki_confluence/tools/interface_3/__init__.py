from .create_approval_request import CreateApprovalRequest
from .decide_approval_step import DecideApprovalStep
from .escalate_to_human import EscalateToHuman
from .manipulate_exports import ManipulateExports
from .manipulate_group_memberships import ManipulateGroupMemberships
from .manipulate_groups import ManipulateGroups
from .manipulate_page_versions import ManipulatePageVersions
from .manipulate_pages import ManipulatePages
from .manipulate_permissions import ManipulatePermissions
from .manipulate_space_features import ManipulateSpaceFeatures
from .manipulate_spaces import ManipulateSpaces
from .manipulate_users import ManipulateUsers
from .manipulate_watchers import ManipulateWatchers
from .record_config_change import RecordConfigChange
from .register_new_audit_trail import RegisterNewAuditTrail
from .retrieve_approval_request import RetrieveApprovalRequest
from .retrieve_config_history import RetrieveConfigHistory
from .retrieve_group import RetrieveGroup
from .retrieve_notifications import RetrieveNotifications
from .retrieve_page import RetrievePage
from .retrieve_permissions import RetrievePermissions
from .retrieve_space import RetrieveSpace
from .retrieve_user import RetrieveUser
from .retrieve_watchers import RetrieveWatchers
from .send_notification import SendNotification

ALL_TOOLS_INTERFACE_3 = [
    CreateApprovalRequest,
    DecideApprovalStep,
    EscalateToHuman,
    ManipulateExports,
    ManipulateGroupMemberships,
    ManipulateGroups,
    ManipulatePageVersions,
    ManipulatePages,
    ManipulatePermissions,
    ManipulateSpaceFeatures,
    ManipulateSpaces,
    ManipulateUsers,
    ManipulateWatchers,
    RecordConfigChange,
    RegisterNewAuditTrail,
    RetrieveApprovalRequest,
    RetrieveConfigHistory,
    RetrieveGroup,
    RetrieveNotifications,
    RetrievePage,
    RetrievePermissions,
    RetrieveSpace,
    RetrieveUser,
    RetrieveWatchers,
    SendNotification
]
