from tau_bench.types import Action, Task

TASKS = [
    Task(
        annotator="0",
        user_id="USR003",
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
    )
]
