from .discover_candidate_entities import DiscoverCandidateEntities
from .discover_interview_offer_entities import DiscoverInterviewOfferEntities
from .manage_employee_operations import ManageEmployeeOperations
from .manage_it_provisioning_operations import ManageItProvisioningOperations
from .manage_offer_operations import ManageOfferOperations
from .manage_onboarding_operations import ManageOnboardingOperations

ALL_TOOLS_INTERFACE_1 = [
    DiscoverCandidateEntities,
    DiscoverInterviewOfferEntities,
    ManageEmployeeOperations,
    ManageItProvisioningOperations,
    ManageOfferOperations,
    ManageOnboardingOperations
]

