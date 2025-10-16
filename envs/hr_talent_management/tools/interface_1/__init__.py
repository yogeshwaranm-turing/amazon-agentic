# interface_1/tool_registry.py
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
from .discover_reference_entities import DiscoverReferenceEntities
from .discover_job_entities import DiscoverJobEntities
from .manage_job_operations import ManageJobOperations
from .manage_candidate_operations import ManageCandidateOperations
from .manage_application_operations import ManageApplicationOperations
from .manage_interview_operations import ManageInterviewOperations
from .discover_employee_entities import DiscoverEmployeeEntities
from .discover_document_task_entities import DiscoverDocumentTaskEntities
from .manage_document_operations import ManageDocumentOperations
from .manage_notification_operations import ManageNotificationOperations
from .create_audit_entry import CreateAuditEntry

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
    DiscoverBenefitEntities,
    DiscoverReferenceEntities,
    DiscoverJobEntities,
    ManageJobOperations,
    ManageCandidateOperations,
    ManageApplicationOperations,
    ManageInterviewOperations,
    DiscoverEmployeeEntities,
    DiscoverDocumentTaskEntities,
    ManageDocumentOperations,
    ManageNotificationOperations,
    CreateAuditEntry,
]
