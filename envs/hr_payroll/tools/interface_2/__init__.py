from .assign_department_manager import AssignDepartmentManager
from .assign_position_to_worker import AssignPositionToWorker
from .check_department_integrity import CheckDepartmentIntegrity
from .create_compliance_action import CreateComplianceAction
from .create_contract import CreateContract
from .generate_heatmap_document import GenerateHeatmapDocument
from .get_compliance_status import GetComplianceStatus
from .get_worker_active_contract import GetWorkerActiveContract
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg


ALL_TOOLS_INTERFACE_2 = [
    AssignDepartmentManager,
    AssignPositionToWorker,
    CheckDepartmentIntegrity,
    CreateComplianceAction,
    CreateContract,
    GenerateHeatmapDocument,
    GetComplianceStatus,
    GetWorkerActiveContract,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
]
