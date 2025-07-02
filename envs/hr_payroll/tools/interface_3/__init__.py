from .list_active_workers import ListActiveWorkers
from .get_worker_contract_summary import GetWorkerContractSummary
from .fetch_team_assignment import FetchTeamAssignment
from .get_invoice_status_by_org import GetInvoiceStatusByOrg
from .retrieve_payroll_breakdown import RetrievePayrollBreakdown
from .update_worker_bank_info import UpdateWorkerBankInfo
from .create_new_invoice import CreateNewInvoice
from .process_reimbursement_request import ProcessReimbursementRequest
from .issue_virtual_card_to_worker import IssueVirtualCardToWorker
from .mark_invoice_as_paid import MarkInvoiceAsPaid
from .terminate_worker_contract import TerminateWorkerContract


ALL_TOOLS_INTERFACE_3 = [
    ListActiveWorkers,
    GetWorkerContractSummary,
    FetchTeamAssignment,
    GetInvoiceStatusByOrg,
    RetrievePayrollBreakdown,
    UpdateWorkerBankInfo,
    CreateNewInvoice,
    ProcessReimbursementRequest,
    IssueVirtualCardToWorker,
    MarkInvoiceAsPaid,
    TerminateWorkerContract,
]
