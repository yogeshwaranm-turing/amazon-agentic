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
from .get_time_entries import GetTimeEntries
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg
from .submit_reimbursement import SubmitReimbursement
from .terminate_worker import TerminateWorker
from .update_organization import UpdateOrganization
from .update_user_profile import UpdateUserProfile
from .update_worker_status import UpdateWorkerStatus
from .validate_reimbursement_limits import ValidateReimbursementLimits
from .calculate_gross_payroll import CalculateGrossPayroll
from .calculate_tax_and_benefits import CalculateTaxAndBenefits
from .add_to_payroll_run import AddToPayrollRun
from .flag_payroll_exception import FlagPayrollException
from .generate_audit_log import GenerateAuditLog
from .finalize_payroll_run import FinalizePayrollRun
from .detect_anomalies import DetectAnomalies
from .lock_time_entry import LockTimeEntry
from .notify_manager import NotifyManager
from .approve_time_entry import ApproveTimeEntry

ALL_TOOLS_INTERFACE_3 = [
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
    GetTimeEntries,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    SubmitReimbursement,
    TerminateWorker,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    ValidateReimbursementLimits,
    CalculateGrossPayroll,
    CalculateTaxAndBenefits,
    AddToPayrollRun,
    FlagPayrollException,
    GenerateAuditLog,
    FinalizePayrollRun,
    DetectAnomalies,
    LockTimeEntry,
    NotifyManager,
    ApproveTimeEntry
]