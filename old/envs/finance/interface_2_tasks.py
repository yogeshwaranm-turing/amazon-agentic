from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="CUST808190",
        instruction="Your user id is CUST808190. You want to open a new checking account. Please proceed to create it.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST808190"
                }
            ),
            Action(
                name="create_account", 
                kwargs={
                    "user_id": "CUST808190", 
                    "account_type": "checking"
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST368317",
        instruction="Your user id is CUST368317. You would like to know the balance in your savings account with ID ACC1331840269, and will like to pay for your invoice with ID INV-240728-nnGt, which costs $1291.07, that was issued to you on the 28th of July, 2024",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST368317"
                }
            ),
            Action(
                name="get_account_balance", 
                kwargs={
                    "account_id": "ACC1331840269"
                }
            ),
            Action(
                name="pay_invoice", 
                kwargs={
                    "invoice_id": "INV-240728-nnGt", 
                    "account_id": "ACC1331840269",
                    "amount": 1291.07
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST459523",
        instruction="Your user id is CUST459523. You would like to void an authorization with ID AUTH310951 on your account with ID ACC1720558072 and also close the same account after the authorization is complete",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST459523"
                }
            ),
            Action(
                name="list_authorization", 
                kwargs={
                    "account_id": "ACC1720558072",
                    "status": "authorized"
                }
            ),
            Action(
                name="void_authorization", 
                kwargs={
                    "auth_id": "AUTH310951"
                }
            ),
            Action(
                name="close_account", 
                kwargs={
                    "account_id": "ACC1720558072"
                }
            ),
        ],
        outputs=[],
    ),
]