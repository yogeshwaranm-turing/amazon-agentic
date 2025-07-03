from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="CUST325963",
        instruction="Your user id is CUST325963. You want to apply for a personal loan of $20,000 at 7.5% interest for 2 years. Please proceed and show me the amortization schedule.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST325963"
                }
            ),
            Action(
                name="apply_loan", 
                kwargs={
                    "user_id": "CUST325963", 
                    "principal": 20000.0, 
                    "interest_rate": 7.5, 
                    "term_years": 2
                }
            ),
            Action(
                name="calculate_amortization", 
                kwargs={
                    "principal": 20000.0, 
                    "interest_rate": 7.5, 
                    "term_years": 2
                }
            ),
        ],
        outputs=[],
    )
]