from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="CUST714697",
        instruction="Your user id is CUST714697. You want to pay for an invoice that is overdue, but need to see all the overdue invoices before you pay. Your invoice ID is CUST714697, and want to pay via your savings account whose ID is ACC1070016762",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST714697"
                }
            ),
            Action(
                name="list_overdue_invoices", 
                kwargs={}
            ),
            Action(
                name="create_invoice_payment", 
                kwargs={
                    "invoice_id": "CUST714697", 
                    "amount": 6181.1, 
                    "account_id": "ACC1070016762"
                }
            ),
        ],
        outputs=[],
    )
]