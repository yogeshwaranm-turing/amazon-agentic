from .tools.assign_department_manager import AssignDepartmentManager
from .tools.assign_position_to_worker import AssignPositionToWorker
from .tools.assign_worker_to_org import AssignWorkerToOrg
from .tools.calculate_amortization import CalculateAmortization
from .tools.check_financial_provider_status import CheckFinancialProviderStatus
from .tools.convert_currency import ConvertCurrency
from .tools.create_department import CreateDepartment
from .tools.create_organization import CreateOrganization
from .tools.create_position import CreatePosition
from .tools.create_user import CreateUser
from .tools.create_worker import CreateWorker
from .tools.deactivate_user import DeactivateUser
from .tools.delete_user import DeleteUser
from .tools.get_bank_account_details import GetBankAccountDetails
from .tools.list_organizations import ListOrganizations
from .tools.list_positions import ListPositions
from .tools.list_users import ListUsers
from .tools.list_users_by_role import ListUsersByRole
from .tools.list_workers_by_org import ListWorkersByOrg
from .tools.record_payment_fx import RecordPaymentFx
from .tools.terminate_worker import TerminateWorker
from .tools.transfer_to_human_agent import TransferToHumanAgent
from .tools.update_organization import UpdateOrganization
from .tools.update_user_profile import UpdateUserProfile
from .tools.update_worker_status import UpdateWorkerStatus
from .tools.validate_provider_route import ValidateProviderRoute

ALL_TOOLS_INTERFACE_5 = [
    AssignDepartmentManager,
    AssignPositionToWorker,
    AssignWorkerToOrg,
    CalculateAmortization,
    CheckFinancialProviderStatus,
    ConvertCurrency,
    CreateDepartment,
    CreateOrganization,
    CreatePosition,
    CreateUser,
    CreateWorker,
    DeactivateUser,
    DeleteUser,
    GetBankAccountDetails,
    ListOrganizations,
    ListPositions,
    ListUsers,
    ListUsersByRole,
    ListWorkersByOrg,
    RecordPaymentFx,
    TerminateWorker,
    TransferToHumanAgent,
    UpdateOrganization,
    UpdateUserProfile,
    UpdateWorkerStatus,
    ValidateProviderRoute,
]