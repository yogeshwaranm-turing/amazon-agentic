from .add_audit_trail import AddAuditTrail
from .add_new_trade_for_fund import AddNewTradeForFund
from .calculate_future_value import CalculateFutureValue
from .calculate_liabilities import CalculateLiabilities
from .calculate_nav import CalculateNav
from .create_fund import CreateFund
from .delete_fund import DeleteFund
from .execute_trade import ExecuteTrade
from .get_approval_by_code import GetApprovalByCode
from .get_available_funds import GetAvailableFunds
from .get_daily_profit_loss_by_fund import GetDailyProfitLossByFund
from .get_fund_instruments import GetFundInstruments
from .get_fund_nav_history import GetFundNavHistory
from .get_fund_trade_details import GetFundTradeDetails
from .get_growth_rate import GetGrowthRate
from .get_instruments import GetInstruments
from .get_instruments_prices import GetInstrumentsPrices
from .get_nav_records import GetNavRecords
from .list_funds_with_filter import ListFundsWithFilter
from .update_fund import UpdateFund
from .update_instrument import UpdateInstrument
from .update_instrument_price import UpdateInstrumentPrice
from .update_nav_record_value import UpdateNavRecordValue
from .update_trade import UpdateTrade

ALL_TOOLS_INTERFACE_1 = [
    AddAuditTrail,
    AddNewTradeForFund,
    CalculateFutureValue,
    CalculateLiabilities,
    CalculateNav,
    CreateFund,
    DeleteFund,
    ExecuteTrade,
    GetApprovalByCode,
    GetAvailableFunds,
    GetDailyProfitLossByFund,
    GetFundInstruments,
    GetFundNavHistory,
    GetFundTradeDetails,
    GetGrowthRate,
    GetInstruments,
    GetInstrumentsPrices,
    GetNavRecords,
    ListFundsWithFilter,
    UpdateFund,
    UpdateInstrument,
    UpdateInstrumentPrice,
    UpdateNavRecordValue,
    UpdateTrade
]
