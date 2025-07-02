# Copyright Sierra

from .book_lounge_access import BookLoungeAccess
from .calculate_baggage_fees import CalculateBaggageFees
from .cancel_upgrade_request import CancelUpgradeRequest
from .get_baggage_policy import GetBaggagePolicy
from .get_boarding_pass import GetBoardingPass
from .list_airport_lounges import ListAirportLounges
from .list_onboard_services import ListOnboardServices
from .list_potential_upgrades import ListPotentialUpgrades
from .list_seat_availability import ListSeatAvailability
from .pay_baggage_fee import PayBaggageFee
from .purchase_onboard_item import PurchaseOnboardItem
from .request_special_meal import RequestSpecialMeal
from .request_upgrade import RequestUpgrade
from .select_seat import SelectSeat
from .send_boarding_pass import SendBoardingPass
from .think import Think
from .transfer_to_human_agents import TransferToHumanAgents
from .update_seat_selection import UpdateSeatSelection


ALL_TOOLS_INTERFACE_4 = [
    BookLoungeAccess,
    CalculateBaggageFees,
    CancelUpgradeRequest,
    GetBaggagePolicy,
    GetBoardingPass,
    ListAirportLounges,
    ListOnboardServices,
    ListPotentialUpgrades,
    ListSeatAvailability,
    PayBaggageFee,
    PurchaseOnboardItem,
    RequestSpecialMeal,
    RequestUpgrade,
    SelectSeat,
    SendBoardingPass,
    Think,
    TransferToHumanAgents,
    UpdateSeatSelection,
]

