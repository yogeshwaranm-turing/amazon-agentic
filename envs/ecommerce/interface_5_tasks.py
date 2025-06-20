from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="USR003",
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
