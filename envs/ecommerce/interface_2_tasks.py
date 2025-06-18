from tau_bench.types import Action, Task

TASKS = [
    Task(
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
    )
]
