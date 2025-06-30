from .assign_department_manager import AssignDepartmentManager
from .assign_device import AssignDevice
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .create_department import CreateDepartment
from .create_organization import CreateOrganization
from .create_position import CreatePosition
from .create_user import CreateUser
from .create_worker import CreateWorker
from .deactivate_user import DeactivateUser
from .decommission_device import DecommissionDevice
from .delete_user import DeleteUser
from .launch_survey import LaunchSurvey
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg
from .submit_engagement_response import SubmitEngagementResponse
from .terminate_worker import TerminateWorker
from .track_device_status import TrackDeviceStatus
from .update_organization import UpdateOrganization
from .update_user_profile import UpdateUserProfile
from .update_worker_status import UpdateWorkerStatus
from .track_response_rates import TrackResponseRates
from .notify_team_lead import NotifyTeamLead
from .flag_team_for_followup import FlagTeamForFollowup
from .record_team_compliance import RecordTeamCompliance
from .create_followup_ticket import CreateFollowupTicket
from .mark_device_status import MarkDeviceStatus

ALL_TOOLS_INTERFACE_4 = [
    AssignDepartmentManager,
    AssignDevice,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CreateDepartment,
    CreateOrganization,
    CreatePosition,
    CreateUser,
    CreateWorker,
    DeactivateUser,
    DecommissionDevice,
    DeleteUser,
    LaunchSurvey,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    SubmitEngagementResponse,
    TerminateWorker,
    TrackDeviceStatus,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    TrackResponseRates,
    NotifyTeamLead,
    FlagTeamForFollowup,
    RecordTeamCompliance,
    CreateFollowupTicket,
    MarkDeviceStatus
]