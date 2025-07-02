from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    # get_user_payment_summary(user_id), remove_payment_method(user_id, method_id)
    Task(
        annotator="0",
        user_id="ava_brown_3860",
        instruction="Your user id is ava_brown_3860. You want to see all your payment summary and then you would like to remove one of your payment methods with ID certificate_2005805",
        actions=[
            Action(
                name="get_user_payment_summary", 
                kwargs={
                    "user_id": "ava_brown_3860"
                }
            ),
            Action(
                name="remove_payment_method", 
                kwargs={
                    "user_id": "ava_brown_3860", 
                    "method_id": "certificate_2005805"
                }
            ),
        ],
        outputs=[],
    ),
]