import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateAuthorization(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      account_id: str, 
      amount: float, 
      currency: str, 
      channel: str="online"
    ) -> str:
        auths = data.setdefault("authorizations", {})
        new_id = f"AUTH{len(auths)+1:06d}"
        now = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        expires = datetime(2025, 1, 7, 0, 0, 0, tzinfo=timezone.utc)
        auth = {
            "auth_id": new_id,
            "account_id": account_id,
            "amount": amount,
            "currency": currency,
            "authorized_at": now.isoformat() + "Z",
            "expires_at": expires.isoformat() + "Z",
            "status": "authorized",
            "merchant": {"name": "Generic Store", "mcc": "5411", "category": "Retail"},
            "channel": channel,
            "card": {"card_type": "Visa", "card_last4": "1234", "card_expiry": "12/27"},
            "geo_location": {"lat": 40.712800, "lng": -74.006000, "city": "New York", "country": "USA"},
            "device_id": "DEV-ABCD-1234",
            "approved_by": "EMP-1001",
            "approved_at": "2025-01-01T01:00:00Z",
            "notes": None
        }
        auths[new_id] = auth
        return json.dumps(auth)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"create_authorization",
            "description":"Place a new card authorization hold on an account.",
            "parameters":{
                "type":"object",
                "properties":{
                    "account_id":{"type":"string"},
                    "amount":{"type":"number"},
                    "currency":{"type":"string"},
                    "channel":{"type":"string"}
                },
                "required":["account_id","amount","currency"]
            }
        }}