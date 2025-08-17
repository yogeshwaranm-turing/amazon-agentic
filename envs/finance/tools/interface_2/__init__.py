from .add_audit_trail import AddAuditTrail
from .add_new_holding import AddNewHolding
from .add_new_user import AddNewUser
from .cancel_subscription import CancelSubscription
from .create_subscription import CreateSubscription
from .find_user import FindUser
from .get_approval_by_code import GetApprovalByCode
from .get_filtered_investors import GetFilteredInvestors
from .get_investor_documents import GetInvestorDocuments
from .get_investor_portfolio import GetInvestorPortfolio
from .get_investor_portfolio_holdings import GetInvestorPortfolioHoldings
from .get_investor_profile import GetInvestorProfile
from .get_investor_redemptions import GetInvestorRedemptions
from .get_investor_statements import GetInvestorStatements
from .get_investor_subscriptions import GetInvestorSubscriptions
from .get_investor_transactions_history import GetInvestorTransactionsHistory
from .get_portfolio_holdings import GetPortfolioHoldings
from .get_subscriptions import GetSubscriptions
from .investor_offboarding import InvestorOffboarding
from .investor_onboarding import InvestorOnboarding
from .process_redemption import ProcessRedemption
from .remove_holding import RemoveHolding
from .switch_funds import SwitchFunds
from .update_investor_details import UpdateInvestorDetails
from .update_investor_portfolio_holding import UpdateInvestorPortfolioHolding
from .update_subscription import UpdateSubscription

ALL_TOOLS_INTERFACE_2 = [
    AddAuditTrail,
    AddNewHolding,
    AddNewUser,
    CancelSubscription,
    CreateSubscription,
    FindUser,
    GetApprovalByCode,
    GetFilteredInvestors,
    GetInvestorDocuments,
    GetInvestorPortfolio,
    GetInvestorPortfolioHoldings,
    GetInvestorProfile,
    GetInvestorRedemptions,
    GetInvestorStatements,
    GetInvestorSubscriptions,
    GetInvestorTransactionsHistory,
    GetPortfolioHoldings,
    GetSubscriptions,
    InvestorOffboarding,
    InvestorOnboarding,
    ProcessRedemption,
    RemoveHolding,
    SwitchFunds,
    UpdateInvestorDetails,
    UpdateInvestorPortfolioHolding,
    UpdateSubscription
]
