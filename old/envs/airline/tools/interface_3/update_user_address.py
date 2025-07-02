import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateUserAddress(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        address1: str = None,
        address2: str = None,
        city: str = None,
        state: str = None,
        zip: str = None,
        country: str = None,
    ) -> str:
        users = data["users"]
        
        if user_id not in users:
            return "Error: user not found"
        addr = users[user_id].setdefault("address", {})

        if address1 is not None:
            addr["address1"] = address1
        if address2 is not None:
            addr["address2"] = address2
        if city is not None:
            addr["city"] = city
        if state is not None:
            addr["state"] = state
        if zip is not None:
            addr["zip"] = zip
        if country is not None:
            addr["country"] = country

        return json.dumps({
            "user_id": user_id,
            "address": addr
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_address",
                "description": "Update one or more fields in a user’s address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "address1": {"type": "string"},
                        "address2": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "zip": {"type": "string"},
                        "country": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }
