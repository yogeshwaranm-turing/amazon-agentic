from .assign_department_manager import AssignDepartmentManager
from .assign_device import AssignDevice
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .create_followup_ticket import CreateFollowupTicket
from .deactivate_user import DeactivateUser
from .decommission_device import DecommissionDevice
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg


ALL_TOOLS_INTERFACE_4 = [
    AssignDepartmentManager,
    AssignDevice,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CreateFollowupTicket,
    DeactivateUser,
    DecommissionDevice,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
]
