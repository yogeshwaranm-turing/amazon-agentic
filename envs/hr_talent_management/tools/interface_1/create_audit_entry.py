# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateAuditEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reference_id: str, reference_type: str, action: str, field_name: str = None, old_value: str = None, new_value: str = None) -> str:
        # Validate enums
        valid_reference_types = [
            "requisition","application","offer","employee","payroll","benefit","exit","document","shortlist"
        ]
        if reference_type not in valid_reference_types:
            raise ValueError(f"Invalid reference_type. Must be one of {valid_reference_types}")

        valid_actions = ["create","update","delete","approve","reject","lock","unlock","submit","verify"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Must be one of {valid_actions}")

        # Create new audit record
        audit_trails = data.setdefault("audit_trails", {})
        new_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
        rec = {
            "audit_id": new_id,
            "reference_id": reference_id,
            "reference_type": reference_type,
            "action": action,
            "user_id": data.get("_caller_user_id", "system"),
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": data.get("_now_utc", "2025-01-01T00:00:00Z"),
        }
        audit_trails[new_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_audit_entry",
                "description": 'Append an audit_trails record (idempotent).',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {"type": "str"},
                        "reference_type": {"type": "str"},
                        "action": {"type": "str"},
                        "field_name": {"type": "str"},
                        "old_value": {"type": "str"},
                        "new_value": {"type": "str"}
                    },
                    "required": ["reference_id", "reference_type", "action"]
                }
            }
        }

# Convenience function wrapper (function-style tool usage)
def create_audit_entry(data: Dict[str, Any], **kwargs) -> str:
    return CreateAuditEntry.invoke(data, **kwargs)
