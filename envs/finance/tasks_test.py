from tau_bench.types import Action, Task

TASKS_TEST = [
    Task(
        annotator="0",
        user_id="CUST770487",
        instruction="Your user id is CUST770487. You want to transfer $500 from your checking account ACC1000000001 to your savings account ACC1000000002. Please confirm and proceed with the transfer.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={"user_id": "CUST770487"}
            ),
            Action(
                name="list_user_accounts", 
                kwargs={"user_id": "CUST770487"}
            ),
            Action(
                name="get_account_details", 
                kwargs={
                    "user_id": "CUST770487", 
                    "account_id": "ACC1000000001", 
                    "account_type": "checking"
                }
            ),
            Action(
                name="get_account_details", 
                kwargs={
                    "user_id": "CUST770487", 
                    "account_id": "ACC1000000002", 
                    "account_type": "savings"
                }
            ),
            Action(
                name="transfer_funds", 
                kwargs={
                    "from_account_id": "ACC1000000001", 
                    "to_account_id": "ACC1000000002", 
                    "amount": 500.0
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST127824",
        instruction="Your user id is CUST127824. You want to apply for a personal loan of $20,000 at 5% interest for 2 years. Please proceed and show me the amortization schedule.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST127824"
                }
            ),
            Action(
                name="apply_loan", 
                kwargs={
                    "user_id": "CUST127824", 
                    "principal": 20000.0, 
                    "interest_rate": 5.0, "term_years": 2
                }
            ),
            Action(
                name="calculate_amortization", 
                kwargs={
                    "principal": 20000.0, 
                    "interest_rate": 5.0, 
                    "term_years": 2
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST629903",
        instruction="Your user id is CUST629903. You want to open a new savings account. Please proceed to create it.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST629903"
                }
            ),
            Action(
                name="create_account", 
                kwargs={
                    "user_id": "CUST629903", 
                    "account_type": "savings"
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST131244",
        instruction="Your user id is CUST131244. You want to view all your loans. Please retrieve your loan list.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST131244"
                }
            ),
            Action(
                name="list_loans", 
                kwargs={
                    "user_id": "CUST131244"
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST809570",
        instruction="Your user id is CUST809570. You want to pay invoice INV-240914-M3N7 from account ACC1000000009 for $236.95 using online payment. Please proceed.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST809570"
                }
            ),
            Action(
                name="list_invoices", 
                kwargs={
                    "user_id": "CUST809570"
                }
            ),
            Action(
                name="pay_invoice", 
                kwargs={
                    "invoice_id": "INV-240914-M3N7", 
                    "account_id": "ACC1000000009", 
                    "amount": 236.95, 
                    "payment_method": "online"
                }
            ),
        ],
        outputs=[],
    ),
]