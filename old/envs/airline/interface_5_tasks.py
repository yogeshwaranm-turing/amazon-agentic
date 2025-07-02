from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="noah_silva_2256",
        instruction="Your user id is noah_silva_2256. You want to get aircraft details with flight number HAT248, and then you will like to subscribe to travel alerts. Lastly, I would also like to suggest that the flight on the 2nd of May, 2024 should be removed since it's status is currently cancelled",
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
            Action(
                name="remove_flight_date_instance", 
                kwargs={
                    "flight_number": "HAT248",
                    "date": "2024-05-02"
                }
            ),
        ],
        outputs=[],
    )
]