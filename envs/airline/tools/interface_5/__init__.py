# Copyright Sierra

from .calculate_baggage_fees import CalculateBaggageFees
from .get_aircraft_details import GetAircraftDetails
from .get_baggage_policy import GetBaggagePolicy
from .get_boarding_pass import GetBoardingPass
from .get_fare_estimate import GetFareEstimate
from .get_travel_advisory import GetTravelAdvisory
from .get_user_itinerary import GetUserItinerary
from .list_potential_upgrades import ListPotentialUpgrades
from .list_seat_availability import ListSeatAvailability
from .send_boarding_pass import SendBoardingPass
from .subscribe_travel_alerts import SubscribeTravelAlerts
from .think import Think
from .transfer_to_human_agents import TransferToHumanAgents
from .update_flight_schedule import UpdateFlightSchedule


ALL_TOOLS_INTERFACE_5 = [
    CalculateBaggageFees,
    GetAircraftDetails,
    GetBaggagePolicy,
    GetBoardingPass,
    GetFareEstimate,
    GetTravelAdvisory,
    GetUserItinerary,
    ListPotentialUpgrades,
    ListSeatAvailability,
    SendBoardingPass,
    SubscribeTravelAlerts,
    Think,
    TransferToHumanAgents,
    UpdateFlightSchedule,
]

