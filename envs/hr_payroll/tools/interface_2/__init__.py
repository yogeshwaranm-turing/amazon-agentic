from .tools.assign_department_manager import AssignDepartmentManager
from .tools.assign_position_to_worker import AssignPositionToWorker
from .tools.assign_worker_to_org import AssignWorkerToOrg
from .tools.create_contract import CreateContract
from .tools.create_department import CreateDepartment
from .tools.create_organization import CreateOrganization
from .tools.create_position import CreatePosition
from .tools.create_user import CreateUser
from .tools.create_worker import CreateWorker
from .tools.deactivate_user import DeactivateUser
from .tools.delete_user import DeleteUser
from .tools.get_compliance_status import GetComplianceStatus
from .tools.get_worker_active_contract import GetWorkerActiveContract
from .tools.list_organizations import ListOrganizations
from .tools.list_positions import ListPositions
from .tools.list_users import ListUsers
from .tools.list_users_by_role import ListUsersByRole
from .tools.list_workers_by_org import ListWorkersByOrg
from .tools.terminate_worker import TerminateWorker
from .tools.transfer_to_human_agent import TransferToHumanAgent
from .tools.update_organization import UpdateOrganization
from .tools.update_user_profile import UpdateUserProfile
from .tools.update_worker_status import UpdateWorkerStatus
from .tools.validate_documents import ValidateDocuments

ALL_TOOLS_INTERFACE_2 = [
    AssignDepartmentManager,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CreateContract,
    CreateDepartment,
    CreateOrganization,
    CreatePosition,
    CreateUser,
    CreateWorker,
    DeactivateUser,
    DeleteUser,
    GetComplianceStatus,
    GetWorkerActiveContract,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    TerminateWorker,
    TransferToHumanAgent,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    ValidateDocuments,
]