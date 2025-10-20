# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from tau_bench.envs.tool import Tool


def _parse_date_sop_mmddyyyy(s: str) -> datetime:
    """
    Parse dates per SOP (MM-DD-YYYY). Raise on invalid.
    """
    try:
        return datetime.strptime(s.strip(), "%m-%d-%Y")
    except Exception as e:
        raise ValueError(f"Invalid date format '{s}'. Expected MM-DD-YYYY.") from e


def _parse_record_dt_flexible(s: str) -> Optional[datetime]:
    """
    Parse record-side timestamps/dates flexibly:
    - ISO 8601: datetime.fromisoformat (YYYY-MM-DD or with time)
    - SOP MM-DD-YYYY
    Returns None if empty/None.
    """
    if not s or not isinstance(s, str) or not s.strip():
        return None
    s = s.strip()
    # Try ISO-8601
    try:
        # fromisoformat supports 'YYYY-MM-DD' and 'YYYY-MM-DDTHH:MM:SS[.fff][+/-offset]'
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        pass
    # Try SOP MM-DD-YYYY (for records that might follow SOP format)
    try:
        return datetime.strptime(s, "%m-%d-%Y")
    except Exception:
        pass
    # Last resort: common formats
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # If unparseable, treat as None (record will just fail date-window checks)
    return None


class DiscoverDocumentTaskEntities(Tool):
    """
    SOP entity discovery for:
      - documents
      - it_provisioning_tasks
    """

    # --- ENUMS FROM DB SCHEMA ---
    DOC_CATEGORIES = {
        'verification_id_proof', 'verification_address_proof', 'verification_educational_certificate',
        'verification_experience_letter', 'verification_work_visa', 'verification_pr_card',
        'verification_bank_proof', 'offer_letter', 'contract', 'policy_acknowledgment', 'tax_form',
        'insurance_form', 'nda', 'resume', 'cover_letter', 'job_description', 'budget_justification',
        'budget_approval', 'workforce_plan', 'recruitment_checklist', 'promotion_letter',
        'transfer_memo', 'other'
    }

    DOC_RELATED_TYPES = {
        'employee', 'candidate', 'offer', 'onboarding', 'job_requisition', 'job_posting', 'application'
    }

    DOC_STATUS = {'active', 'archived', 'expired'}
    DOC_VERIFICATION_STATUS = {'pending', 'verified', 'failed'}

    IT_TASK_TYPES = {'email_account', 'laptop', 'access_badge', 'system_access', 'software_license'}
    IT_TASK_STATUS = {'pending', 'in_progress', 'completed', 'failed'}

    # --- ALLOWED FILTERS PER SOP ---
    DOC_ALLOWED_FILTERS = {
        "document_id",
        "document_category",
        "related_entity_type",
        "related_entity_id",
        "file_name",
        "upload_date_from",
        "upload_date_to",
        "uploaded_by",
        "document_status",
        "expiry_date_from",
        "expiry_date_to",
        "verification_status",
        "verified_by",
    }

    IT_ALLOWED_FILTERS = {
        "task_id",
        "employee_id",
        "task_type",
        "task_status",
        "assigned_by",              # DB has 'assigned_by' (SOP text mentions 'assigned_to'—use schema)
        "completion_date_from",
        "completion_date_to",
    }

    @staticmethod
    def _validate_filters(entity_type: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate filter names and enum values; normalize enum strings to lowercase.
        Raises ValueError on any invalid input.
        """
        if entity_type == "documents":
            allowed = DiscoverDocumentTaskEntities.DOC_ALLOWED_FILTERS
        elif entity_type == "it_provisioning_tasks":
            allowed = DiscoverDocumentTaskEntities.IT_ALLOWED_FILTERS
        else:
            raise ValueError("Invalid entity_type. Must be one of {'documents','it_provisioning_tasks'}.")

        # Unknown filter keys -> error (SOP: halt on invalid)
        unknown = set(filters.keys()) - allowed
        if unknown:
            raise ValueError(f"Unknown filters for {entity_type}: {sorted(unknown)}")

        # Normalize enums (lowercase string) and validate
        f = dict(filters)  # copy

        if entity_type == "documents":
            # enums: document_category, related_entity_type, document_status, verification_status
            if "document_category" in f and f["document_category"] is not None:
                v = str(f["document_category"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_CATEGORIES:
                    raise ValueError(f"Invalid document_category. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_CATEGORIES)}")
                f["document_category"] = v

            if "related_entity_type" in f and f["related_entity_type"] is not None:
                v = str(f["related_entity_type"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_RELATED_TYPES:
                    raise ValueError(f"Invalid related_entity_type. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_RELATED_TYPES)}")
                f["related_entity_type"] = v

            if "document_status" in f and f["document_status"] is not None:
                v = str(f["document_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_STATUS:
                    raise ValueError(f"Invalid document_status. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_STATUS)}")
                f["document_status"] = v

            if "verification_status" in f and f["verification_status"] is not None:
                v = str(f["verification_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_VERIFICATION_STATUS:
                    raise ValueError(f"Invalid verification_status. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_VERIFICATION_STATUS)}")
                f["verification_status"] = v

            # Date range inputs must be SOP MM-DD-YYYY if present
            for k in ("upload_date_from", "upload_date_to", "expiry_date_from", "expiry_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        elif entity_type == "it_provisioning_tasks":
            if "task_type" in f and f["task_type"] is not None:
                v = str(f["task_type"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.IT_TASK_TYPES:
                    raise ValueError(f"Invalid task_type. Allowed: {sorted(DiscoverDocumentTaskEntities.IT_TASK_TYPES)}")
                f["task_type"] = v

            if "task_status" in f and f["task_status"] is not None:
                v = str(f["task_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.IT_TASK_STATUS:
                    raise ValueError(f"Invalid task_status. Allowed: {sorted(DiscoverDocumentTaskEntities.IT_TASK_STATUS)}")
                f["task_status"] = v

            # Date range inputs must be SOP MM-DD-YYYY if present
            for k in ("completion_date_from", "completion_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        return f

    @staticmethod
    def _range_match(rec_value: Optional[str], start: Optional[datetime], end: Optional[datetime]) -> bool:
        """
        Generic date window check: record value may be ISO or SOP; filters are datetime (or None).
        """
        if start is None and end is None:
            return True
        rv = _parse_record_dt_flexible(rec_value)
        if rv is None:
            return False
        if start is not None and rv < start:
            return False
        if end is not None and rv > end:
            return False
        return True

    @staticmethod
    def _paginate(items: List[Dict[str, Any]], limit: int, offset: int) -> Dict[str, Any]:
        end = offset + limit
        sliced = items[offset:end]
        next_offset = end if end < len(items) else None
        return {"items": sliced, "next_offset": next_offset}

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        # --- Normalize basic params ---
        entity_type = (entity_type or "").strip().lower()
        if entity_type not in {"documents", "it_provisioning_tasks"}:
            raise ValueError("Invalid entity_type. Must be one of {'documents','it_provisioning_tasks'}.")

        limit = int(limit or 50)
        offset = int(offset or 0)
        if limit <= 0:
            raise ValueError("limit must be > 0.")
        if offset < 0:
            raise ValueError("offset must be >= 0.")

        filters = filters or {}
        if not isinstance(filters, dict):
            raise ValueError("filters must be an object/dict.")

        f = DiscoverDocumentTaskEntities._validate_filters(entity_type, filters)

        # --- Fetch and filter ---
        out: List[Dict[str, Any]] = []

        if entity_type == "documents":
            docs = data.get("documents", {})
            for _, d in docs.items():
                # direct equals filters
                if "document_id" in f and f["document_id"] and d.get("document_id") != f["document_id"]:
                    continue
                if "related_entity_type" in f and f["related_entity_type"] and \
                        str(d.get("related_entity_type", "")).lower() != f["related_entity_type"]:
                    continue
                if "related_entity_id" in f and f["related_entity_id"] and d.get("related_entity_id") != f["related_entity_id"]:
