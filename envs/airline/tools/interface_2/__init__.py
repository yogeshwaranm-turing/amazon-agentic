# Copyright Sierra

from .add_passenger import AddPassenger
from .apply_promo_code import ApplyPromoCode
from .calculate_change_fee import CalculateChangeFee
from .cancel_passenger import CancelPassenger
from .cancel_upgrade_request import CancelUpgradeRequest
from .check_in import CheckIn
from .get_available_flights import GetAvailableFlights
from .get_fare_estimate import GetFareEstimate
from .get_reservation_details import GetReservationDetails
from .get_user_itinerary import GetUserItinerary
from .purchase_reservation_insurance import PurchaseReservationInsurance
from .remove_saved_passenger import RemoveSavedPassenger
from .request_upgrade import RequestUpgrade
from .think import Think
from .transfer_reservation_owner import TransferReservationOwner
from .transfer_to_human_agents import TransferToHumanAgents
from .update_flight_schedule import UpdateFlightSchedule
from .update_reservation_flight_type import UpdateReservationFlightType


ALL_TOOLS_INTERFACE_2 = [
    AddPassenger,
    ApplyPromoCode,
    CalculateChangeFee,
    CancelPassenger,
    CancelUpgradeRequest,
    CheckIn,
    GetAvailableFlights,
    GetFareEstimate,
    GetReservationDetails,
    GetUserItinerary,
    PurchaseReservationInsurance,
    RemoveSavedPassenger,
    RequestUpgrade,
    Think,
    TransferReservationOwner,
    TransferToHumanAgents,
    UpdateFlightSchedule,
    UpdateReservationFlightType,
]
