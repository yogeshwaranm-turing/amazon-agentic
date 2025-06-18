from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    # get_customer_details, list_assets_by_vendor, update_asset_details
    Task(
        annotator="0",
        user_id="CUST325963",
        instruction="Your user id is CUST325963. You made a mistake when entering the details of your asset and want to change the vendor from Hoover, Mcneil and Wilson to Unilever PLC",
        actions=[
            Action(
                name="get_customer_details", 
                kwargs={
                    "user_id": "CUST325963"
                }
            ),
            Action(
                name="list_assets_by_vendor", 
                kwargs={
                    "vendor": "Hoover, Mcneil and Wilson"
                }
            ),
            Action(
                name="update_asset_details", 
                kwargs={
                    "asset_id": "VEH-CHI-2624",
                    "updates": {
                        "vendor": "Unilever"
                    }
                }
            ),
        ],
        outputs=[],
    )
]