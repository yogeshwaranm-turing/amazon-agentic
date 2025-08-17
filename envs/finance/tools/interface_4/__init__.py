from .add_audit_trail import AddAuditTrail
from .add_new_user import AddNewUser
from .calculate_future_value import CalculateFutureValue
from .calculate_nav import CalculateNav
from .create_fund import CreateFund
from .create_upload_document import CreateUploadDocument
from .delete_fund import DeleteFund
from .generate_report import GenerateReport
from .get_approval_by_code import GetApprovalByCode
from .get_available_funds import GetAvailableFunds
from .get_commitments import GetCommitments
from .get_daily_profit_loss_by_fund import GetDailyProfitLossByFund
from .get_fund_instruments import GetFundInstruments
from .get_fund_trade_details import GetFundTradeDetails
from .get_growth_rate import GetGrowthRate
from .get_instruments import GetInstruments
from .get_instruments_prices import GetInstrumentsPrices
from .get_nav_records import GetNavRecords
from .get_performance_history import GetPerformanceHistory
from .list_funds_with_filter import ListFundsWithFilter
from .summary_of_instrument_types_by_prices import SummaryOfInstrumentTypesByPrices
from .update_fund import UpdateFund
from .update_instrument import UpdateInstrument
from .update_instrument_price import UpdateInstrumentPrice
from .update_nav_record_value import UpdateNavRecordValue

ALL_TOOLS_INTERFACE_4 = [
    AddAuditTrail,
    AddNewUser,
    CalculateFutureValue,
    CalculateNav,
    CreateFund,
    CreateUploadDocument,
    DeleteFund,
    GenerateReport,
    GetApprovalByCode,
    GetAvailableFunds,
    GetCommitments,
    GetDailyProfitLossByFund,
    GetFundInstruments,
    GetFundTradeDetails,
    GetGrowthRate,
    GetInstruments,
    GetInstrumentsPrices,
    GetNavRecords,
    GetPerformanceHistory,
    ListFundsWithFilter,
    SummaryOfInstrumentTypesByPrices,
    UpdateFund,
    UpdateInstrument,
    UpdateInstrumentPrice,
    UpdateNavRecordValue
]
