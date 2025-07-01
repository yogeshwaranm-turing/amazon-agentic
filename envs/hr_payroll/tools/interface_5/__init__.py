from .assign_department_manager import AssignDepartmentManager
from .assign_position_to_worker import AssignPositionToWorker
from .assign_worker_to_org import AssignWorkerToOrg
from .calculate_amortization import CalculateAmortization
from .check_financial_provider_status import CheckFinancialProviderStatus
from .check_for_linked_payments import CheckForLinkedPayments
from .get_bank_account_details import GetBankAccountDetails
from .list_organizations import ListOrganizations
from .list_positions import ListPositions
from .list_users import ListUsers
from .list_users_by_role import ListUsersByRole
from .list_workers_by_org import ListWorkersByOrg


ALL_TOOLS_INTERFACE_5 = [
    AssignDepartmentManager,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CalculateAmortization,
    CheckFinancialProviderStatus,
    CheckForLinkedPayments,
    GetBankAccountDetails,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
]
