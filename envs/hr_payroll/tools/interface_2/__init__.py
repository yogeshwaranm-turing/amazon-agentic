from .assign_department_manager import AssignDepartmentManager
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .create_contract import CreateContract
from .create_department import CreateDepartment
from .create_organization import CreateOrganization
from .create_position import CreatePosition
from .create_user import CreateUser
from .create_worker import CreateWorker
from .deactivate_user import DeactivateUser
from .delete_user import DeleteUser
from .get_compliance_status import GetComplianceStatus
from .get_worker_active_contract import GetWorkerActiveContract
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg
from .terminate_worker import TerminateWorker
from .update_organization import UpdateOrganization
from .update_user_profile import UpdateUserProfile
from .update_worker_status import UpdateWorkerStatus
from .validate_documents import ValidateDocuments

from .filter_expiring_contracts_within_days import FilterExpiringContractsWithinDays
from .notify_hr_team import NotifyHrTeam
from .send_termination_notice import SendTerminationNotice
from .create_compliance_action import CreateComplianceAction
from .assign_to_hr import AssignToHr
from .send_worker_reminder import SendWorkerReminder
from .group_by_organization_and_severity import GroupByOrganizationAndSeverity
from .identify_critical_unresolved import IdentifyCriticalUnresolved
from .generate_heatmap_document import GenerateHeatmapDocument
from .store_document import StoreDocument
from .email_report import EmailReport

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
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    ValidateDocuments,
    FilterExpiringContractsWithinDays,
    NotifyHrTeam,
    SendTerminationNotice,
    CreateComplianceAction,
    AssignToHr,
    SendWorkerReminder,
    GroupByOrganizationAndSeverity,
    IdentifyCriticalUnresolved,
    GenerateHeatmapDocument,
    StoreDocument,
    EmailReport
]