# Copyright Sierra

from .add_payment_method import AddPaymentMethod
from .delete_user_account import DeleteUserAccount
from .enroll_loyalty_member import EnrollLoyaltyMember
from .get_loyalty_balance import GetLoyaltyBalance
from .get_membership_tier import GetMembershipTier
from .get_travel_advisory import GetTravelAdvisory
from .get_user_details import GetUserDetails
from .get_user_payment_summary import GetUserPaymentSummary
from .redeem_loyalty_miles import RedeemLoyaltyMiles
from .remove_payment_method import RemovePaymentMethod
from .subscribe_travel_alerts import SubscribeTravelAlerts
from .think import Think
from .transfer_to_human_agents import TransferToHumanAgents
from .update_contact_information import UpdateContactInformation
from .update_user_address import UpdateUserAddress


ALL_TOOLS_INTERFACE_3 = [
    AddPaymentMethod,
    DeleteUserAccount,
    EnrollLoyaltyMember,
    GetLoyaltyBalance,
    GetMembershipTier,
    GetTravelAdvisory,
    GetUserDetails,
    GetUserPaymentSummary,
    RedeemLoyaltyMiles,
    RemovePaymentMethod,
    SubscribeTravelAlerts,
    Think,
    TransferToHumanAgents,
    UpdateContactInformation,
    UpdateUserAddress,
]

