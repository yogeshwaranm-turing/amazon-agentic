# Auto-generated — DO NOT EDIT BY HAND
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from tau_bench.envs.tool import Tool


def _parse_date_sop_mmddyyyy(s: str) -> datetime:
    """Parse dates per SOP (MM-DD-YYYY). Raise on invalid."""
    try:
        return datetime.strptime(s.strip(), "%m-%d-%Y")
    except Exception as e:
        raise ValueError(f"Invalid date format '{s}'. Expected MM-DD-YYYY.") from e


def _parse_record_dt_flexible(s: str) -> Optional[datetime]:
    """
    Parse record-side timestamps/dates flexibly:
    - ISO 8601 (YYYY-MM-DD or with time / Z)
    - SOP MM-DD-YYYY
    Returns None if empty/None or unparseable.
    """
    if not s or not isinstance(s, str) or not s.strip():
        return None
    s = s.strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        pass
    try:
        return datetime.strptime(s, "%m-%d-%Y")
    except Exception:
        pass
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return None


class DiscoverDocumentTaskEntities(Tool):
    """
    SOP discovery for:
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
        "assigned_by",              # DB has 'assigned_by' (SOP text mentioned assigned_to; schema wins)
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

        f = dict(filters)  # copy / normalized

        if entity_type == "documents":
            if "document_category" in f and f["document_category"] is not None:
                v = str(f["document_category"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_CATEGORIES:
                    raise ValueError(
                        f"Invalid document_category. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_CATEGORIES)}"
                    )
                f["document_category"] = v

            if "related_entity_type" in f and f["related_entity_type"] is not None:
                v = str(f["related_entity_type"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_RELATED_TYPES:
                    raise ValueError(
                        f"Invalid related_entity_type. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_RELATED_TYPES)}"
                    )
                f["related_entity_type"] = v

            if "document_status" in f and f["document_status"] is not None:
                v = str(f["document_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_STATUS:
                    raise ValueError(
                        f"Invalid document_status. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_STATUS)}"
                    )
                f["document_status"] = v

            if "verification_status" in f and f["verification_status"] is not None:
                v = str(f["verification_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.DOC_VERIFICATION_STATUS:
                    raise ValueError(
                        f"Invalid verification_status. Allowed: {sorted(DiscoverDocumentTaskEntities.DOC_VERIFICATION_STATUS)}"
                    )
                f["verification_status"] = v

            for k in ("upload_date_from", "upload_date_to", "expiry_date_from", "expiry_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        elif entity_type == "it_provisioning_tasks":
            if "task_type" in f and f["task_type"] is not None:
                v = str(f["task_type"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.IT_TASK_TYPES:
                    raise ValueError(
                        f"Invalid task_type. Allowed: {sorted(DiscoverDocumentTaskEntities.IT_TASK_TYPES)}"
                    )
                f["task_type"] = v

            if "task_status" in f and f["task_status"] is not None:
                v = str(f["task_status"]).lower().strip()
                if v not in DiscoverDocumentTaskEntities.IT_TASK_STATUS:
                    raise ValueError(
                        f"Invalid task_status. Allowed: {sorted(DiscoverDocumentTaskEntities.IT_TASK_STATUS)}"
                    )
                f["task_status"] = v

            for k in ("completion_date_from", "completion_date_to"):
                if k in f and f[k] is not None:
                    f[k] = _parse_date_sop_mmddyyyy(str(f[k]))

        return f

    @staticmethod
    def _range_match(rec_value: Optional[str], start: Optional[datetime], end: Optional[datetime]) -> bool:
        """Generic date window check using parsed datetimes."""
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
        return {"items": sliced, "count": len(items), "next_offset": next_offset}

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
                if "document_id" in f and f["document_id"] and d.get("document_id") != f["document_id"]:
                    continue
                if "related_entity_type" in f and f["related_entity_type"] and \
                        str(d.get("related_entity_type", "")).lower() != f["related_entity_type"]:
                    continue
                if "related_entity_id" in f and f["related_entity_id"] and d.get("related_entity_id") != f["related_entity_id"]:
                    continue
                if "document_category" in f and f["document_category"] and \
                        str(d.get("document_category", "")).lower() != f["document_category"]:
                    continue
                if "file_name" in f and f["file_name"] and d.get("file_name") != f["file_name"]:
                    continue
                if "uploaded_by" in f and f["uploaded_by"] and d.get("uploaded_by") != f["uploaded_by"]:
                    continue
                if "document_status" in f and f["document_status"] and \
                        str(d.get("document_status", "")).lower() != f["document_status"]:
                    continue
                if "verification_status" in f and f["verification_status"] and \
                        str(d.get("verification_status", "")).lower() != f["verification_status"]:
                    continue
                if "verified_by" in f and f["verified_by"] and d.get("verified_by") != f["verified_by"]:
                    continue

                # Date windows
                if not DiscoverDocumentTaskEntities._range_match(
                    d.get("upload_date"), f.get("upload_date_from"), f.get("upload_date_to")
                ):
                    continue
                if not DiscoverDocumentTaskEntities._range_match(
                    d.get("expiry_date"), f.get("expiry_date_from"), f.get("expiry_date_to")
                ):
                    continue

                out.append(d)

            page = DiscoverDocumentTaskEntities._paginate(out, limit, offset)
            page.update({"entity_type": "documents", "filters_applied": filters})
            return json.dumps(page)

        # it_provisioning_tasks
        tasks = data.get("it_provisioning_tasks", {})
        for _, t in tasks.items():
            if "task_id" in f and f["task_id"] and t.get("task_id") != f["task_id"]:
                continue
            if "employee_id" in f and f["employee_id"] and t.get("employee_id") != f["employee_id"]:
                continue
            if "task_type" in f and f["task_type"] and str(t.get("task_type", "")).lower() != f["task_type"]:
                continue
            if "task_status" in f and f["task_status"] and str(t.get("task_status", "")).lower() != f["task_status"]:
                continue
            if "assigned_by" in f and f["assigned_by"] and t.get("assigned_by") != f["assigned_by"]:
                continue
            if not DiscoverDocumentTaskEntities._range_match(
                t.get("completion_date"), f.get("completion_date_from"), f.get("completion_date_to")
            ):
                continue

            out.append(t)

        page = DiscoverDocumentTaskEntities._paginate(out, limit, offset)
        page.update({"entity_type": "it_provisioning_tasks", "filters_applied": filters})
        return json.dumps(page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns a structured schema with explicit types AND examples so callers know exactly how to use this tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "discover_document_task_entities",
                "description": (
                    "Discover 'documents' or 'it_provisioning_tasks' per SOP/DB. "
                    "All date filter inputs must be MM-DD-YYYY. "
                    "Response includes items, count, next_offset, filters_applied, and entity_type."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "enum": ["documents", "it_provisioning_tasks"],
                            "description": "Which entity bucket to search."
                        },
                        "filters": {
                            "type": "object",
                            "description": (
                                "Filter object (all fields optional). "
                                "For 'documents', allowed keys: "
                                "document_id, document_category, related_entity_type, related_entity_id, file_name, "
                                "upload_date_from, upload_date_to, uploaded_by, document_status, "
                                "expiry_date_from, expiry_date_to, verification_status, verified_by. "
                                "For 'it_provisioning_tasks', allowed keys: "
                                "task_id, employee_id, task_type, task_status, assigned_by, "
                                "completion_date_from, completion_date_to."
                            ),
                            "properties": {
                                # Documents
                                "document_id": {"type": "string", "description": "Exact document id."},
                                "document_category": {
                                    "type": "string",
                                    "enum": sorted(list(DOC_CATEGORIES)),
                                    "description": "Document category (enum from DB)."
                                },
                                "related_entity_type": {
                                    "type": "string",
                                    "enum": sorted(list(DOC_RELATED_TYPES)),
                                    "description": "Related entity type (enum from DB)."
                                },
                                "related_entity_id": {"type": "string", "description": "Related entity id."},
                                "file_name": {"type": "string", "description": "Exact file name match."},
                                "upload_date_from": {"type": "string", "description": "MM-DD-YYYY"},
                                "upload_date_to": {"type": "string", "description": "MM-DD-YYYY"},
                                "uploaded_by": {"type": "string", "description": "Uploader user_id."},
                                "document_status": {
                                    "type": "string",
                                    "enum": sorted(list(DOC_STATUS)),
                                    "description": "Document status (enum)."
                                },
                                "expiry_date_from": {"type": "string", "description": "MM-DD-YYYY"},
                                "expiry_date_to": {"type": "string", "description": "MM-DD-YYYY"},
                                "verification_status": {
                                    "type": "string",
                                    "enum": sorted(list(DOC_VERIFICATION_STATUS)),
                                    "description": "Verification status (enum)."
                                },
                                "verified_by": {"type": "string", "description": "Verifier user_id."},

                                # IT tasks
                                "task_id": {"type": "string", "description": "Exact task id."},
                                "employee_id": {"type": "string", "description": "Employee id owning the task."},
                                "task_type": {
                                    "type": "string",
                                    "enum": sorted(list(IT_TASK_TYPES)),
                                    "description": "IT provisioning task type (enum)."
                                },
                                "task_status": {
                                    "type": "string",
                                    "enum": sorted(list(IT_TASK_STATUS)),
                                    "description": "IT task status (enum)."
                                },
                                "assigned_by": {"type": "string", "description": "Assigning user_id (per DB schema)."},
                                "completion_date_from": {"type": "string", "description": "MM-DD-YYYY"},
                                "completion_date_to": {"type": "string", "description": "MM-DD-YYYY"},
                            }
                        },
                        "limit": {"type": "integer", "description": "Max items to return (default 50)."},
                        "offset": {"type": "integer", "description": "Starting index for pagination (default 0)."}
                    },
                    "required": ["entity_type"]
                },
                # Concrete examples (helps tool UIs / callers)
                "examples": [
                    {
                        "name": "Search documents by type and date range",
                        "payload": {
                            "entity_type": "documents",
                            "filters": {
                                "document_category": "offer_letter",
                                "related_entity_type": "offer",
                                "upload_date_from": "09-01-2025",
                                "upload_date_to": "10-15-2025",
                                "document_status": "active"
                            },
                            "limit": 25,
                            "offset": 0
                        }
                    },
                    {
                        "name": "Find completed laptop tasks in Q3 window",
                        "payload": {
                            "entity_type": "it_provisioning_tasks",
                            "filters": {
                                "task_type": "laptop",
                                "task_status": "completed",
                                "completion_date_from": "07-01-2025",
                                "completion_date_to": "09-30-2025"
                            },
                            "limit": 100,
                            "offset": 0
                        }
                    }
                ],
                # Response shape docs (handy for consumers)
                "returns": {
                    "type": "object",
                    "description": "Paginated results",
                    "properties": {
                        "items": {"type": "array", "description": "List of matched entities."},
                        "count": {"type": "integer", "description": "Total matched (pre-pagination)."},
                        "next_offset": {"type": ["integer", "null"], "description": "Next offset or null if exhausted."},
                        "filters_applied": {"type": "object", "description": "Echo of input filters."},
                        "entity_type": {"type": "string", "enum": ["documents", "it_provisioning_tasks"]}
                    }
                }
            }
        }
