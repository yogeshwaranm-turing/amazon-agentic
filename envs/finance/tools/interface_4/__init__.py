
from .apply_loan import ApplyLoan
from .calculate_amortization import CalculateAmortization
from .calculate_total_depreciation import CalculateTotalDepreciation
from .close_loan import CloseLoan
from .get_loan_amortization_schedule import GetLoanAmortizationSchedule
from .get_loan_details import GetLoanDetails
from .get_loan_portfolio_summary import GetLoanPortfolioSummary
from .payoff_loan import PayoffLoan
from .refinance_loan import RefinanceLoan
from .transfer_to_human_agents import TransferToHumanAgents
from .update_loan_terms import UpdateLoanTerms


ALL_TOOLS_INTERFACE_4 = [
    ApplyLoan,
    CalculateAmortization,
    CalculateTotalDepreciation,
    CloseLoan,
    GetLoanAmortizationSchedule,
    GetLoanDetails,
    GetLoanPortfolioSummary,
    PayoffLoan,
    RefinanceLoan,
    TransferToHumanAgents,
    UpdateLoanTerms,
]
