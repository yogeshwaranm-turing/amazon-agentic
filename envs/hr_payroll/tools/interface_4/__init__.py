from .tools.assign_department_manager import AssignDepartmentManager
from .tools.assign_device import AssignDevice
from .tools.assign_position_to_worker import AssignPositionToWorker
from .tools.assign_worker_to_org import AssignWorkerToOrg
from .tools.create_department import CreateDepartment
from .tools.create_organization import CreateOrganization
from .tools.create_position import CreatePosition
from .tools.create_user import CreateUser
from .tools.create_worker import CreateWorker
from .tools.deactivate_user import DeactivateUser
from .tools.decommission_device import DecommissionDevice
from .tools.delete_user import DeleteUser
from .tools.launch_survey import LaunchSurvey
from .tools.list_organizations import ListOrganizations
from .tools.list_positions import ListPositions
from .tools.list_users import ListUsers
from .tools.list_users_by_role import ListUsersByRole
from .tools.list_workers_by_org import ListWorkersByOrg
from .tools.submit_engagement_response import SubmitEngagementResponse
from .tools.terminate_worker import TerminateWorker
from .tools.track_device_status import TrackDeviceStatus
from .tools.transfer_to_human_agent import TransferToHumanAgent
from .tools.update_organization import UpdateOrganization
from .tools.update_user_profile import UpdateUserProfile
from .tools.update_worker_status import UpdateWorkerStatus

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
    TransferToHumanAgent,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
]