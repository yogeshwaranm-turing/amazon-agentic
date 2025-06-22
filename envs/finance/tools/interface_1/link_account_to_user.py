import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class LinkAccountToUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        account_id: str,
        user_id: str,
        relationship_type: str = "primary"
    ) -> str:
        accounts = data.get("accounts", {})
        users = data.get("users", {})
        
        # Validate account exists
        if account_id not in accounts:
            raise ValueError(f"Account {account_id} not found.")
        
        # Validate user exists
        if user_id not in users:
            raise ValueError(f"User {user_id} not found.")
        
        account = accounts[account_id]
        
        # Check if account is already linked to a different user
        current_user = account.get("user_id")
        if current_user and current_user != user_id:
            # Create joint account relationship instead of changing ownership
            joint_users = account.get("joint_users", [])
            if user_id not in joint_users:
                joint_users.append(user_id)
                account["joint_users"] = joint_users
                account["joint_added_at"] = datetime.now().isoformat() + "Z"
            
            result = {
                "account_id": account_id,
                "primary_user": current_user,
                "joint_users": joint_users,
                "relationship_type": "joint",
                "linked_at": datetime.now().isoformat() + "Z"
            }
        else:
            # Link account to user as primary
            account["user_id"] = user_id
            account["relationship_type"] = relationship_type
            account["linked_at"] = datetime.now().isoformat() + "Z"
            
            result = {
                "account_id": account_id,
                "user_id": user_id,
                "relationship_type": relationship_type,
                "linked_at": datetime.now().isoformat() + "Z"
            }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "link_account_to_user",
                "description": "Associate additional accounts to existing users with proper validation and joint account support.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "user_id": {"type": "string"},
                        "relationship_type": {"type": "string", "enum": ["primary", "joint", "beneficiary"]}
                    },
                    "required": ["account_id", "user_id"]
                }
            }
        }
