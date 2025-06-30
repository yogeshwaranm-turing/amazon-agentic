# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)

def load_data() -> dict[str, Any]:
    file_names = [
        "users.json",
        "organizations.json",
        "workers.json",
        "contracts.json",
        "payrolls.json",
        "payments.json",
        "devices.json",
        "reimbursements.json",
        "compliance_records.json",
        "documents.json",
        "locations.json",
        "financial_providers.json",
        "bank_accounts.json",
        "virtual_cards.json",
        "engagement_records.json",
        "team_memberships.json",
        "time_entries.json",
        "assets.json",
        "asset_assignments.json",
    ]

    dataset: dict[str, Any] = {}

    for file_name in file_names:
        path = os.path.join(FOLDER_PATH, file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                key = file_name.replace(".json", "")
                dataset[key] = json.load(f)
        else:
            print(f"Warning: {file_name} not found in {FOLDER_PATH}, skipping.")

    return dataset
