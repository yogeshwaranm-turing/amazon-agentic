from .add_to_payroll_run import AddToPayrollRun
from .approve_time_entry import ApproveTimeEntry
from .assign_department_manager import AssignDepartmentManager
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .generate_audit_log import GenerateAuditLog
from .get_time_entries import GetTimeEntries
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg


ALL_TOOLS_INTERFACE_3 = [
    AddToPayrollRun,
    ApproveTimeEntry,
    AssignDepartmentManager,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    GenerateAuditLog,
    GetTimeEntries,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
]
