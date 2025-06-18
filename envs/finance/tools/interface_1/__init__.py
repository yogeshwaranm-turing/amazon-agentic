

from .create_user import CreateUser
from .delete_user import DeleteUser
from .get_account_details import GetAccountDetails
from .get_customer_details import GetCustomerDetails
from .list_loans import ListLoans
from .list_invoices import ListInvoices
from .list_transactions import ListTransactions
from .list_user_accounts import ListUserAccounts
from .transfer_funds import TransferFunds
from .transfer_to_human_agents import TransferToHumanAgents
from .update_user_profile import UpdateUserProfile


ALL_TOOLS_INTERFACE_1 = [
    CreateUser,
    DeleteUser,
    GetAccountDetails,
    GetCustomerDetails,
    ListLoans,
    ListInvoices,
    ListTransactions,
    ListUserAccounts,
    TransferFunds,
    TransferToHumanAgents,
    UpdateUserProfile,
]
