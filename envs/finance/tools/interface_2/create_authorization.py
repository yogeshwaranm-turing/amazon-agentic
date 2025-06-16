import json, random
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from faker import Faker
from tau_bench.envs.tool import Tool

fake = Faker()

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
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=7)
        auth = {
            "auth_id": new_id,
            "account_id": account_id,
            "amount": amount,
            "currency": currency,
            "authorized_at": now.isoformat() + "Z",
            "expires_at": expires.isoformat() + "Z",
            "status": "authorized",
            "merchant": {"name": fake.company(), "mcc": f"{random.randint(1000,9999)}", "category": fake.random_element(elements=["Retail","Travel","Food","Healthcare"])},
            "channel": channel,
            "card": {"card_type": random.choice(["Visa","Mastercard","Amex","Discover"]), "card_last4": f"{random.randint(0,9999):04d}", "card_expiry": fake.credit_card_expire(end="+3y")},
            "geo_location": {"lat": round(random.uniform(25.0,49.0),6), "lng": round(random.uniform(-124.0,-66.0),6), "city": fake.city(), "country": "USA"},
            "device_id": fake.lexify(text="DEV-????-????"),
            "approved_by": f"EMP-{random.randint(1000,9999)}",
            "approved_at": (now + timedelta(hours=1)).isoformat() + "Z",
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