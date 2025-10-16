from .discover_candidate_entities import DiscoverCandidateEntities
from .discover_interview_offer_entities import DiscoverInterviewOfferEntities
from .manage_employee_operations import ManageEmployeeOperations
from .manage_it_provisioning_operations import ManageItProvisioningOperations
from .manage_offer_operations import ManageOfferOperations
from .manage_onboarding_operations import ManageOnboardingOperations
from .manage_payroll_cycle_operations import ManagePayrollCycleOperations
from .manage_payroll_input_operations import ManagePayrollInputOperations
from .manage_payroll_earning_operations import ManagePayrollEarningOperations
from .manage_payslip_operations import ManagePayslipOperations
from .discover_payroll_entities import DiscoverPayrollEntities
from .discover_benefit_entities import DiscoverBenefitEntities

ALL_TOOLS_INTERFACE_1 = [
    DiscoverCandidateEntities,
    DiscoverInterviewOfferEntities,
    ManageEmployeeOperations,
    ManageItProvisioningOperations,
    ManageOfferOperations,
    ManageOnboardingOperations,
    ManagePayrollCycleOperations,
    ManagePayrollInputOperations,
    ManagePayrollEarningOperations,
    ManagePayslipOperations,
    DiscoverPayrollEntities,
    DiscoverBenefitEntities
]
