from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="noah_jackson_7027",
        instruction="Your user id is noah_jackson_7027. You want to get your boarding pass and also pay your baggage fee for your reservation with ID OLXVJQ, and pay with your credit card credit_card_3909926.",
        actions=[
            Action(
                name="get_boarding_pass", 
                kwargs={
                    "reservation_id": "OLXVJQ"
                }
            ),
            Action(
                name="pay_baggage_fee", 
                kwargs={
                    "reservation_id": "OLXVJQ", 
                    "payment_method": "credit_card_3909926"
                }
            ),
        ],
        outputs=[],
    ),
]