from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="CUST642669",
        instruction="Your user id is CUST642669. You want to transfer $500 from your checking account ACC1775242831 to your savings account ACC1340318275. Please confirm and proceed with the transfer.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={"user_id": "CUST642669"}
            ),
            Action(
                name="list_user_accounts", 
                kwargs={"user_id": "CUST642669"}
            ),
            Action(
                name="get_account_details", 
                kwargs={
                    "user_id": "CUST642669", 
                    "account_id": "ACC1775242831", 
                    "account_type": "checking"
                }
            ),
            Action(
                name="get_account_details", 
                kwargs={
                    "user_id": "CUST642669", 
                    "account_id": "ACC1340318275", 
                    "account_type": "savings"
                }
            ),
            Action(
                name="transfer_funds", 
                kwargs={
                    "from_account_id": "ACC1775242831", 
                    "to_account_id": "ACC1340318275", 
                    "amount": 500.0
                }
            ),
        ],
        outputs=[],
    )
]