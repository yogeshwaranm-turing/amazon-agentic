from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="olivia_moore_2080",
        instruction="Your user id is olivia_moore_2080. You would like to get a list of all your itinery and then get details on your reservation with ID SF5VA1, which would then prompt you to request an upgrade to business class on your reservation",
        actions=[
            Action(
                name="get_user_itinery", 
                kwargs={
                    "user_id": "olivia_moore_2080"
                }
            ),
            Action(
                name="get_reservation_details", 
                kwargs={
                    "reservation_id": "SF5VA1"
                }
            ),
            Action(
                name="request_upgrade", 
                kwargs={
                    "reservation_id": "SF5VA1", 
                    "upgrade_to": "business"
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="1",
        user_id="olivia_moore_2080",
        instruction="Your user id is olivia_moore_2080. You want to get your itinery, and then ask to apply a promo code DISCOUNT10 to your reservation SF5VA1, then you would like to get your reservation details again to inspect your information",
        actions=[
            Action(
                name="get_user_itinery", 
                kwargs={
                    "user_id": "olivia_moore_2080"
                }
            ),
            Action(
                name="apply_promo_code", 
                kwargs={
                    "reservation_id": "SF5VA1",
                    "promo_code": "DISCOUNT10"
                }
            ),
            Action(
                name="get_reservation_details", 
                kwargs={
                    "reservation_id": "SF5VA1"
                }
            )
        ],
        outputs=[],
    ),
    # Task(
    #     annotator="2",
    #     user_id="olivia_moore_2080",
    #     instruction="Your user id is olivia_moore_2080. You would like to get your reservation details with a reservation ID SF5VA1, and then you would like to add a passenger to your reservation whose name is Sammy Sunderlands, born on 2nd of December, 1980",
    #     actions=[
    #         Action(
    #             name="get_reservation_details", 
    #             kwargs={
    #                 "reservation_id": "SF5VA1"
    #             }
    #         ),
    #         Action(
    #             name="add_passenger", 
    #             kwargs={
    #                 "reservation_id": "SF5VA1",
    #                 "first_name": "Sammy",
    #                 "last_name": "Sunderlands",
    #                 "dob": "1980-12-02",
    #             }
    #         ),
    #     ],
    #     outputs=[],
    # ),
]