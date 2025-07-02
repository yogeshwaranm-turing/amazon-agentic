
from .close_account import CloseAccount
from .consolidate_user_accounts import ConsolidateUserAccounts
from .create_account import CreateAccount
from .create_loan import CreateLoan
from .create_user import CreateUser
from .delete_loan import DeleteLoan
from .delete_user import DeleteUser
from .get_account_details import GetAccountDetails
from .get_customer_details import GetCustomerDetails
from .link_account_to_user import LinkAccountToUser
from .list_invoices import ListInvoices
from .list_loans import ListLoans
from .list_transactions import ListTransactions
from .list_user_accounts import ListUserAccounts
from .process_interest_accrual import ProcessInterestAccrual
from .process_loan_payment import ProcessLoanPayment
from .transfer_funds import TransferFunds
from .transfer_to_human_agents import TransferToHumanAgents
from .update_account_status import UpdateAccountStatus
from .update_loan_status import UpdateLoanStatus
from .update_user_profile import UpdateUserProfile


ALL_TOOLS_INTERFACE_1 = [
    CloseAccount,
    ConsolidateUserAccounts,
    CreateAccount,
    CreateLoan,
    CreateUser,
    DeleteLoan,
    DeleteUser,
    GetAccountDetails,
    GetCustomerDetails,
    LinkAccountToUser,
    ListInvoices,
    ListLoans,
    ListTransactions,
    ListUserAccounts,
    ProcessInterestAccrual,
    ProcessLoanPayment,
    TransferFunds,
    TransferToHumanAgents,
    UpdateAccountStatus,
    UpdateLoanStatus,
    UpdateUserProfile,
]
