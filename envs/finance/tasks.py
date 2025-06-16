tasks = [
    {
        "annotator": 0,
        "user_id": "CUST770487",
        "instruction": "Your user id is CUST770487. You want to transfer $500 from your checking account ACC1000000001 to your savings account ACC1000000002. Please confirm and proceed with the transfer.",
        "actions": [
            {"name": "get_customer_details", "arguments": {"user_id": "CUST770487"}},
            {"name": "list_user_accounts", "arguments": {"user_id": "CUST770487"}},
            {"name": "get_account_details", "arguments": {"user_id": "CUST770487", "account_id": "ACC1000000001", "account_type": "checking"}},
            {"name": "get_account_details", "arguments": {"user_id": "CUST770487", "account_id": "ACC1000000002", "account_type": "savings"}},
            {"name": "transfer_funds", "arguments": {"from_account_id": "ACC1000000001", "to_account_id": "ACC1000000002", "amount": 500.0}},
        ],
    }
]