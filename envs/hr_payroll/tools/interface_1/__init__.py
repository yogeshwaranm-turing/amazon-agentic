from .assign_department_manager import AssignDepartmentManager
from .assign_worker_to_org import AssignWorkerToOrg
from .create_alignment_review import CreateAlignmentReview
from .deactivate_user import DeactivateUser
from .delete_user import DeleteUser
from .fetch_worker_details import FetchWorkerDetails
from .generate_user_invite_token import GenerateUserInviteToken
from .get_department_worker_summary import GetDepartmentWorkerSummary
from .list_organizations import ListOrganizations
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg
from .set_worker_position_info import SetWorkerPositionInfo
from .validate_worker_structure import ValidateWorkerStructure


ALL_TOOLS_INTERFACE_1 = [
    AssignDepartmentManager,
    AssignWorkerToOrg,
    CreateAlignmentReview,
    DeactivateUser,
    DeleteUser,
    FetchWorkerDetails,
    GenerateUserInviteToken,
    GetDepartmentWorkerSummary,
    ListOrganizations,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    SetWorkerPositionInfo,
    ValidateWorkerStructure,
]
