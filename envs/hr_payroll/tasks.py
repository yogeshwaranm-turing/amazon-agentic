tasks = [
    {
        "annotator": 0,
        "user_id": "usr_10001_04",
        "instruction": (
            "Your user ID is usr_10001_04. You are submitting a reimbursement of $950 for a business event. "
            "Please first confirm your worker record is active. Then verify that your reimbursement policy allows amounts over $800. "
            "After that, check if your linked bank account is active and the associated financial provider is currently operational. "
            "If all validations succeed, proceed to submit the reimbursement using the linked bank account."
        ),
        "actions": [
            {
                "name": "get_user_profile",
                "arguments": {
                    "user_id": "usr_10001_04"
                }
            },
            {
                "name": "get_worker_details_by_user",
                "arguments": {
                    "user_id": "usr_10001_04"
                }
            },
            {
                "name": "check_reimbursement_policy_limit",
                "arguments": {
                    "amount": 950.0
                }
            },
            {
                "name": "list_user_bank_accounts",
                "arguments": {
                    "user_id": "usr_10001_04"
                }
            },
            {
                "name": "get_bank_account_details",
                "arguments": {
                    "user_id": "usr_10001_04",
                    "bank_account_id": "bact_10001_04"
                }
            },
            {
                "name": "check_financial_provider_status",
                "arguments": {
                    "provider_id": "prov_10001_04"
                }
            },
            {
                "name": "submit_reimbursement_request",
                "arguments": {
                    "worker_id": "wrk_10001_04",
                    "organization_id": "org_10001_04",
                    "amount": 950.0,
                    "currency": "USD",
                    "submit_date": "2025-06-30",
                    "payment_method": "bank_account",
                    "bank_account_id": "bact_10001_04"
                }
            },
        ]
    }
]
