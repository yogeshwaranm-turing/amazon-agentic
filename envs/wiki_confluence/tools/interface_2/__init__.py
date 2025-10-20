from .create_approval_request import CreateApprovalRequest
from .create_new_audit_trail import CreateNewAuditTrail
from .decide_approval_step import DecideApprovalStep
from .fetch_approval_request import FetchApprovalRequest
from .fetch_config_history import FetchConfigHistory
from .fetch_group import FetchGroup
from .fetch_notifications import FetchNotifications
from .fetch_page import FetchPage
from .fetch_permissions import FetchPermissions
from .fetch_space import FetchSpace
from .fetch_user import FetchUser
from .fetch_watchers import FetchWatchers
from .record_config_change import RecordConfigChange
from .send_notification import SendNotification
from .set_exports import SetExports
from .set_group_memberships import SetGroupMemberships
from .set_groups import SetGroups
from .set_page_versions import SetPageVersions
from .set_pages import SetPages
from .set_permissions import SetPermissions
from .set_space_features import SetSpaceFeatures
from .set_spaces import SetSpaces
from .set_users import SetUsers
from .set_watchers import SetWatchers
from .switch_to_human import SwitchToHuman

ALL_TOOLS_INTERFACE_2 = [
    CreateApprovalRequest,
    CreateNewAuditTrail,
    DecideApprovalStep,
    FetchApprovalRequest,
    FetchConfigHistory,
    FetchGroup,
    FetchNotifications,
    FetchPage,
    FetchPermissions,
    FetchSpace,
    FetchUser,
    FetchWatchers,
    RecordConfigChange,
    SendNotification,
    SetExports,
    SetGroupMemberships,
    SetGroups,
    SetPageVersions,
    SetPages,
    SetPermissions,
    SetSpaceFeatures,
    SetSpaces,
    SetUsers,
    SetWatchers,
    SwitchToHuman
]
