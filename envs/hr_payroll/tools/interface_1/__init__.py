from .assign_department_manager import AssignDepartmentManager
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .create_department import CreateDepartment
from .create_organization import CreateOrganization
from .create_position import CreatePosition
from .create_user import CreateUser
from .create_worker import CreateWorker
from .deactivate_user import DeactivateUser
from .delete_user import DeleteUser
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg
from .terminate_worker import TerminateWorker
from .update_organization import UpdateOrganization
from .update_user_profile import UpdateUserProfile
from .update_worker_status import UpdateWorkerStatus
from .compare_worker_and_position_departments import CompareWorkerAndPositionDepartments
from .create_alignment_review import CreateAlignmentReview
from .notify_department_head import NotifyDepartmentHead
from .log_department_alignment_ok import LogDepartmentAlignmentOk

ALL_TOOLS_INTERFACE_1 = [
    AssignDepartmentManager,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CreateDepartment,
    CreateOrganization,
    CreatePosition,
    CreateUser,
    CreateWorker,
    DeactivateUser,
    DeleteUser,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    TerminateWorker,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    CompareWorkerAndPositionDepartments,
    CreateAlignmentReview,
    NotifyDepartmentHead,
    LogDepartmentAlignmentOk
]