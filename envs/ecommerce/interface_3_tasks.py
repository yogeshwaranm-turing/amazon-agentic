from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="USR003",
        instruction="User USR003 - email taylor.williams003@example.com wants to modify the purchase order PO0001, product PRD0001 with new quantity is 10",
        actions=[
            Action(
                name="modify_quantity_of_purchase_order_item",
                kwargs={
                    "purchase_order_id": "PO0001",
                    "product_id": "PRD0001",
                    "new_quantity": 10,
                },
            )
        ],
        outputs=[],
    )
]
