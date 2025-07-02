
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class InitiateWorkerOnboarding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, org_id: str) -> str:
        users = data.get("users", {})
        orgs = data.get("organizations", {})
        if user_id not in users:
            raise ValueError("User not found")
        if org_id not in orgs:
            raise ValueError("Organization not found")
        if users[user_id]["status"] in ["suspended", "pending"]:
            raise ValueError("User is not eligible for onboarding")

        if any(w["user_id"] == user_id for w in data.get("workers", {}).values()):
            raise ValueError("User already linked to a worker")

        worker_id = str(uuid.uuid4())
        workers = data.setdefault("workers", {})
        workers[worker_id] = {
            "user_id": user_id,
            "organization_id": org_id,
            "worker_type": "employee",
            "status": "onboarding"
        }
        return json.dumps({"worker_id": worker_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "initiate_worker_onboarding",
                "description": "Links a user to a worker and organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user to onboard"
                        },
                        "org_id": {
                            "type": "string",
                            "description": "Organization ID for assignment"
                        }
                    },
                    "required": ["user_id", "org_id"]
                }
            }
        }
