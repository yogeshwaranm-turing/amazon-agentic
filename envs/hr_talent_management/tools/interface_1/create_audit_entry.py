# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateAuditEntry(Tool):
    """
    Create an audit trail record consistent with the HR SOP and DB schema.
    - Enforces valid reference_type and action enums (DB-aligned).
    - Requires a caller user id for traceability (SOP: auditable, role-bound actions).
    - Uses UTC ISO8601 timestamps for created_at (DB: timestamp).
    - For 'update' actions, requires field_name and at least one of old_value/new_value.
    - Normalizes enums to lowercase to reduce caller error, while validating against allowed sets.
    """

    VALID_REFERENCE_TYPES = {
        "requisition", "application", "offer", "employee", "payroll",
        "benefit", "exit", "document", "shortlist"
    }

    VALID_ACTIONS = {
        "create", "update", "delete", "approve", "reject",
        "lock", "unlock", "submit", "verify"
    }

    @staticmethod
    def _now_utc_iso(data: Dict[str, Any]) -> str:
        # Prefer injected clock for determinism in tests; otherwise real UTC
        injected = data.get("_now_utc")
        if isinstance(injected, str) and injected.strip():
            return injected
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _require_caller_user_id(data: Dict[str, Any]) -> str:
        caller = data.get("_caller_user_id")
        if not caller or not isinstance(caller, str) or not caller.strip():
            # SOP: halt with explicit error if we cannot attribute the action
            raise ValueError("Missing _caller_user_id for audit attribution.")
        return caller

    @staticmethod
    def _next_numeric_id_str(store: Dict[str, Any]) -> str:
        # Tolerate non-numeric keys; increment max of numeric keys
        numeric_keys = [int(k) for k in store.keys() if str(k).isdigit()]
        return str((max(numeric_keys) if numeric_keys else 0) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reference_id: str,
        reference_type: str,
        action: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> str:
        # -------- Input normalization --------
        if not isinstance(reference_id, str) or not reference_id.strip():
            raise ValueError("Invalid reference_id. Must be a non-empty string.")

        ref_type_norm = reference_type.lower().strip() if isinstance(reference_type, str) else ""
        action_norm = action.lower().strip() if isinstance(action, str) else ""

        if ref_type_norm not in CreateAuditEntry.VALID_REFERENCE_TYPES:
            raise ValueError(
                f"Invalid reference_type. Must be one of {sorted(CreateAuditEntry.VALID_REFERENCE_TYPES)}"
            )
        if action_norm not in CreateAuditEntry.VALID_ACTIONS:
            raise ValueError(
                f"Invalid action. Must be one of {sorted(CreateAuditEntry.VALID_ACTIONS)}"
            )

        # For 'update', require field_name and at least one of old/new
        if action_norm == "update":
            if not field_name or not isinstance(field_name, str) or not field_name.strip():
                raise ValueError("For action 'update', field_name is required.")
            if (old_value is None) and (new_value is None):
                raise ValueError("For action 'update', at least one of old_value or new_value must be provided.")

        # -------- Caller + time --------
        caller_user_id = CreateAuditEntry._require_caller_user_id(data)
        created_at_iso = CreateAuditEntry._now_utc_iso(data)

        # -------- Storage --------
        audit_trails = data.setdefault("audit_trails", {})
        new_id = CreateAuditEntry._next_numeric_id_str(audit_trails)

        rec = {
            "audit_id": new_id,
            "reference_id": reference_id,
            "reference_type": ref_type_norm,
            "action": action_norm,
            "user_id": caller_user_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": created_at_iso,
        }

        audit_trails[new_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        # Use proper JSON Schema primitive types ("string")
        return {
            "type": "function",
            "function": {
                "name": "create_audit_entry",
                "description": "Append a record to audit_trails adhering to HR audit policy.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reference_id": {"type": "string"},
                        "reference_type": {"type": "string"},
                        "action": {"type": "string"},
                        "field_name": {"type": "string"},
                        "old_value": {"type": "string"},
                        "new_value": {"type": "string"},
                    },
                    "required": ["reference_id", "reference_type", "action"],
                },
            },
        }


def create_audit_entry(data: Dict[str, Any], **kwargs) -> str:
    return CreateAuditEntry.invoke(data, **kwargs)
