from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="noah_silva_2256",
        instruction="Your user id is noah_silva_2256. You want to get aircraft details with flight number HAT248, and then you will like to subscribe to travel alerts",
        actions=[
            Action(
                name="get_aircraft_details", 
                kwargs={
                    "flight_number": "HAT248"
                }
            ),
            Action(
                name="subscribe_travel_alerts", 
                kwargs={
                    "user_id": "noah_silva_2256"
                }
            ),
        ],
        outputs=[],
    )
]