from tau_bench.types import Action, Task

TASKS = [
    Task(
        annotator="0",
        user_id="USR003",
        instruction="User USR003 - email taylor.williams003@example.com wants to place an order for product PRD0002 with quantity 3.",
        actions=[
            Action(
                name="place_order",
                kwargs={
                    "user_id": "USR003",
                    "order_date": "2024-06-01",
                    "items": [
                        {"product_id": "PRD0002", "quantity": 3, "unit_price": 45.0}
                    ],
                },
            )
        ],
        outputs=["SO0011", "Pending"],
    ),
    Task(
        annotator="0",
        user_id="USR003",
        instruction="User USR003 - email taylor.williams003@example.com wants to modify the order SO0001, product PRD0001 with new quantity is 10",
        actions=[
            Action(
                name="modify_sales_order_item",
                kwargs={
                    "sales_order_id": "SO0001",
                    "product_id": "PRD0001",
                    "new_quantity": 10,
                },
            )
        ],
        outputs=[],
    ),
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
    ),
    Task(
        annotator="0",
        user_id="USR821",
        instruction="User USR821 - email alex.turner821@example.com wants to delivery the shipment for the tracking number TRK302527, order SO0455.",
        actions=[
            Action(
                name="delivery_shipment",
                kwargs={
                     "tracking_number": "TRK302527"
                },
            )
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="USR821",
        instruction="User USR821 - email alex.turner821@example.com wants to delete the sales order SO0455.",
        actions=[
            Action(
                name="delete_sales_order_by_id",
                kwargs={
                     "sales_order_id": "SO0455"
                },
            )
        ],
        outputs=[],
    )
]
