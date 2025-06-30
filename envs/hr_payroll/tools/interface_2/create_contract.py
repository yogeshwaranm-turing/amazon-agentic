import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateContract(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str,
        organization_id: str,
        user_id: str,
        start_date: str,
        end_date: str,
        rate: float,
        rate_type: str,
        currency: str
    ) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})
        users = data.get("users", {})
        contracts = data.setdefault("contracts", {})

        if worker_id not in workers:
            raise ValueError(f"Worker ID '{worker_id}' not found.")
        if organization_id not in organizations:
            raise ValueError(f"Organization ID '{organization_id}' not found.")
        if user_id not in users:
            raise ValueError(f"User ID '{user_id}' not found.")

        if rate_type not in ["hourly", "monthly", "weekly", "annual"]:
            raise ValueError("rate_type must be one of: hourly, monthly, weekly, annual")

        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError("currency must be a 3-letter ISO currency code")

        # Generate contract_id like contract_0001
        suffix = 1
        while f"contract_{suffix}" in contracts:
            suffix += 1
        contract_id = f"contract_{suffix}"

        now = datetime.now(timezone.utc).isoformat()

        new_contract = {
            "worker_id": worker_id,
            "organization_id": organization_id,
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "rate": rate,
            "rate_type": rate_type,
            "currency": currency,
            "status": "active",
            "created_at": now,
            "updated_at": now
        }

        contracts[contract_id] = new_contract
        return json.dumps({**new_contract, "contract_id": contract_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_contract",
                "description": "Create a new contract for a worker including pay and duration.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string"},
                        "organization_id": {"type": "string"},
                        "user_id": {"type": "string"},
                        "start_date": {"type": "string", "format": "date"},
                        "end_date": {"type": "string", "format": "date"},
                        "rate": {"type": "number"},
                        "rate_type": {
                            "type": "string",
                            "enum": ["hourly", "monthly", "weekly", "annual"]
                        },
                        "currency": {"type": "string"}
                    },
                    "required": [
                        "worker_id", "organization_id", "user_id",
                        "start_date", "end_date", "rate", "rate_type", "currency"
                    ]
                }
            }
        }
