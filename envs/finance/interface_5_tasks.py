from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="CUST325963",
        instruction="Your user id is CUST325963. You made a mistake when entering the details of your asset and want to change the vendor from Perez Group to Unilever PLC. After that, you want to dispose of the asset SFT-MIA-7447 on 2025-01-01T00:00:00 and get the proceeds of 1000.0. The disposal method is 'donation' and the reason for disposal is 'end of life'",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST325963"
                }
            ),
            Action(
                name="list_assets", 
                kwargs={
                    "user_id": "CUST325963"
                }
            ),
            Action(
                name="update_asset_details", 
                kwargs={
                    "asset_id": "SFT-MIA-7447",
                    "updates": {
                        "vendor": "Unilever PLC"
                    }
                }
            ),
            Action(
                name="dispose_asset", 
                kwargs={
                    "asset_id": "SFT-MIA-7447",
                    "disposed_at": "2025-01-01T00:00:00",
                    "proceeds": 1000.0,
                    "disposal_method": "donation",
                    "disposal_reason": "end of life"
                }
            ),
        ],
        outputs=[],
    ),
    Task(
        annotator="0",
        user_id="CUST772519",
        instruction="Your user id is CUST772519. You want to list all your assets and then get the depreciation schedule for the asset SFT-LAX-8994.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST772519"
                }
            ),
            Action(
                name="list_assets", 
                kwargs={
                    "user_id": "CUST772519"
                }
            ),
            Action(
                name="get_depreciation_schedule", 
                kwargs={
                    "asset_id": "SFT-LAX-8994"
                }
            )
        ],
        outputs=[],
    ),
    # Let's have a task to get user details and then assign the asset to another user. Confirm both user details and asset assignment.
    Task(
        annotator="0",
        user_id="CUST772519",
        instruction="Your user id is CUST772519. You want to get your user details and then assign the asset SFT-LAX-8994 to another user with id CUST841069.",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST772519"
                }
            ),
            Action(
                name="list_assets", 
                kwargs={
                    "user_id": "CUST772519"
                }
            ),
            Action(
                name="assign_asset_to_user", 
                kwargs={
                    "asset_id": "SFT-LAX-8994",
                    "user_id": "CUST841069"
                }
            )
        ],
        outputs=[],
    ),
]