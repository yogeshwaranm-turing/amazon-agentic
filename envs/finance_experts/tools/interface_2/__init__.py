from .check_approval import CheckApproval
from .add_commitment import AddCommitment
from .add_investor import AddInvestor
from .add_new_audit_trail import AddNewAuditTrail
from .search_billing_entities import SearchBillingEntities
from .search_fund_entities import SearchFundEntities
from .search_instrument_entities import SearchInstrumentEntities
from .search_investment_flow_entities import SearchInvestmentFlowEntities
from .search_investor_entities import SearchInvestorEntities
from .search_portfolio_entities import SearchPortfolioEntities
from .search_reporting_entities import SearchReportingEntities
from .search_system_entities import SearchSystemEntities
from .search_trading_entities import SearchTradingEntities
from .search_user_entities import SearchUserEntities
from .search_valuation_entities import SearchValuationEntities
from .execute_trade import ExecuteTrade
from .settle_commitment import SettleCommitment
from .generate_report import GenerateReport
from .handle_fund import HandleFund
from .handle_instrument import HandleInstrument
from .handle_instrument_price import HandleInstrumentPrice
from .handle_invoice import HandleInvoice
from .handle_nav_record import HandleNavRecord
from .handle_notifications import HandleNotifications
from .handle_payment import HandlePayment
from .handle_portfolio import HandlePortfolio
from .handle_portfolio_holdings import HandlePortfolioHoldings
from .handle_subscription import HandleSubscription
from .terminate_investor import TerminateInvestor
from .process_redemption import ProcessRedemption
from .switch_to_human import SwitchToHuman  
from .insert_document import InsertDocument

ALL_TOOLS_INTERFACE_2 = [
    CheckApproval,
    AddCommitment,
    AddInvestor,
    AddNewAuditTrail,
    SearchBillingEntities,
    SearchFundEntities,
    SearchInstrumentEntities,
    SearchInvestmentFlowEntities,
    SearchInvestorEntities,
    SearchPortfolioEntities,
    SearchReportingEntities,
    SearchSystemEntities,
    SearchTradingEntities,
    SearchUserEntities,
    SearchValuationEntities,
    ExecuteTrade,
    SettleCommitment,
    GenerateReport,
    HandleFund,
    HandleInstrument,
    HandleInstrumentPrice,
    HandleInvoice,
    HandleNavRecord,
    HandleNotifications,
    HandlePayment,
    HandlePortfolio,
    HandlePortfolioHoldings,
    HandleSubscription,
    TerminateInvestor,
    ProcessRedemption,
    SwitchToHuman,
    InsertDocument
]
