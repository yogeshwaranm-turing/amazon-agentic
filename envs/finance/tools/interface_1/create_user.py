import json
import random
from datetime import datetime, timezone
from typing import Any, Dict
from faker import Faker
from tau_bench.envs.tool import Tool

fake = Faker()

class CreateUser(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      first_name: str, 
      last_name: str, 
      email: str, 
      date_of_birth: str, 
      phone_number: str, 
      address: Dict[str, Any]
    ) -> str:
        users = data["users"]
        
        max_id = max([int(uid[4:]) for uid in users.keys() if uid.startswith("CUST")] + [100000])
        new_id = f"CUST{max_id + 1}"
        now_iso = datetime.now(timezone.utc).isoformat()
        
        new_user = {
            "user_id": new_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "date_of_birth": date_of_birth,
            "phone_number": phone_number,
            "address": address,
            "created_at": now_iso,
            "updated_at": now_iso,
            "last_login_at": now_iso,
            "kyc_status": random.choice(["verified","pending","rejected"]),
            "preferred_contact_method": random.choice(["email","sms"]),
            "marketing_opt_in": fake.boolean(chance_of_getting_true=50),
            "time_zone": fake.timezone(),
            "risk_score": random.randint(300,850),
            "ssn_last4": f"{random.randint(0,9999):04d}"
        }
        
        users[new_id] = new_user
        
        return json.dumps(new_user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "create_user",
            "description": "Create a new customer profile with defaults.",
            "parameters": {
              "type": "object",
              "properties": {
                "first_name": {
                  "type": "string"
                },
                "last_name": {
                  "type": "string"
                },
                "email": {
                  "type": "string",
                  "format": "email"
                },
                "date_of_birth": {
                  "type": "string",
                  "format": "date"
                },
                "phone_number": {
                  "type": "string"
                },
                "address": {
                  "type": "object",
                  "properties": {
                    "street": {
                      "type": "string"
                    },
                    "city": {
                      "type": "string"
                    },
                    "state": {
                      "type": "string"
                    },
                    "postal_code": {
                      "type": "string"
                    },
                    "country": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "street",
                    "city",
                    "state",
                    "postal_code",
                    "country"
                  ]
                }
              },
              "required": [
                "first_name",
                "last_name",
                "email",
                "date_of_birth",
                "phone_number",
                "address"
              ]
            }
          }
        }