from .approval_lookup import ApprovalLookup
from .generate_commitment import GenerateCommitment
from .generate_investor import GenerateInvestor
from .generate_new_audit_trail import GenerateNewAuditTrail
from .get_billing_entities import GetBillingEntities
from .get_fund_entities import GetFundEntities
from .get_instrument_entities import GetInstrumentEntities
from .get_investment_flow_entities import GetInvestmentFlowEntities
from .get_investor_entities import GetInvestorEntities
from .get_portfolio_entities import GetPortfolioEntities
from .get_reporting_entities import GetReportingEntities
from .get_system_entities import GetSystemEntities
from .get_trading_entities import GetTradingEntities
from .get_user_entities import GetUserEntities
from .get_valuation_entities import GetValuationEntities
from .execute_trade import ExecuteTrade
from .fulfill_commitment import FulfillCommitment
from .generate_report import GenerateReport
from .process_fund import ProcessFund
from .process_instrument import ProcessInstrument
from .process_instrument_price import ProcessInstrumentPrice
from .process_invoice import ProcessInvoice
from .process_nav_record import ProcessNavRecord
from .process_notifications import ProcessNotifications
from .process_payment import ProcessPayment
from .process_portfolio import ProcessPortfolio
from .process_portfolio_holdings import ProcessPortfolioHoldings
from .process_subscription import ProcessSubscription
from .offboard_investor import OffboardInvestor
from .process_redemption import ProcessRedemption
from .transfer_to_human_agents import TransferToHumanAgents
from .upload_document import UploadDocument

ALL_TOOLS_INTERFACE_1 = [
    ApprovalLookup,
    GenerateCommitment,
    GenerateInvestor,
    GenerateNewAuditTrail,
    GetBillingEntities,
    GetFundEntities,
    GetInstrumentEntities,
    GetInvestmentFlowEntities,
    GetInvestorEntities,
    GetPortfolioEntities,
    GetReportingEntities,
    GetSystemEntities,
    GetTradingEntities,
    GetUserEntities,
    GetValuationEntities,
    ExecuteTrade,
    FulfillCommitment,
    GenerateReport,
    ProcessFund,
    ProcessInstrument,
    ProcessInstrumentPrice,
    ProcessInvoice,
    ProcessNavRecord,
    ProcessNotifications,
    ProcessPayment,
    ProcessPortfolio,
    ProcessPortfolioHoldings,
    ProcessSubscription,
    OffboardInvestor,
    ProcessRedemption,
    TransferToHumanAgents,
    UploadDocument
]
