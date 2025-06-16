tasks = [
    {
        # New task: place an order for a product
        "annotator": 0,
        "user_id": "USR003",
        "instruction": "User USR003 - email taylor.williams003@example.com wants to place an order for product PRD0002 with quantity 3.",
        "actions": [
            {
                "name": "place_order",
                "arguments": {
                    "user_id": "USR003",
                    "order_date": "2024-06-01",
                    "items": [
                        {
                            "product_id": "PRD0002",
                            "quantity": 3,
                            "unit_price": 45.0
                        }
                    ]
                },
            },
        ]
    }
]
