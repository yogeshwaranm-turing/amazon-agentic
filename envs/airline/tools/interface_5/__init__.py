# Copyright Sierra

from .add_flight import AddFlight
from .calculate_baggage_fees import CalculateBaggageFees
from .create_reservation import CreateReservation
from .delete_reservation import DeleteReservation
from .get_aircraft_details import GetAircraftDetails
from .get_baggage_policy import GetBaggagePolicy
from .get_boarding_pass import GetBoardingPass
from .get_fare_estimate import GetFareEstimate
from .get_travel_advisory import GetTravelAdvisory
from .get_user_itinerary import GetUserItinerary
from .list_potential_upgrades import ListPotentialUpgrades
from .list_seat_availability import ListSeatAvailability
from .remove_flight_date_instance import RemoveFlightDateInstance
from .send_boarding_pass import SendBoardingPass
from .subscribe_travel_alerts import SubscribeTravelAlerts
from .think import Think
from .transfer_to_human_agents import TransferToHumanAgents
from .update_flight_schedule import UpdateFlightSchedule
from .update_flight_status import UpdateFlightStatus


ALL_TOOLS_INTERFACE_5 = [
    AddFlight,
    CalculateBaggageFees,
    CreateReservation,
    DeleteReservation,
    GetAircraftDetails,
    GetBaggagePolicy,
    GetBoardingPass,
    GetFareEstimate,
    GetTravelAdvisory,
    GetUserItinerary,
    ListPotentialUpgrades,
    ListSeatAvailability,
    RemoveFlightDateInstance,
    SendBoardingPass,
    SubscribeTravelAlerts,
    Think,
    TransferToHumanAgents,
    UpdateFlightSchedule,
    UpdateFlightStatus,
]

