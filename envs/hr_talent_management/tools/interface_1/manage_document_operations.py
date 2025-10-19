# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageDocumentOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], mode: str, document_category: str = None, related_entity_type: str = None, related_entity_id: str = None, file_name: str = None, file_format: str = None, uploaded_by: str = None, document_id: str = None, expiry_date: str = None, verification_status: str = None, document_status: str = None) -> str:
        documents = data.setdefault("documents", {})
        mode = (mode or "").strip().lower()
        if mode not in {"documents.create","documents.verify","documents.update_status"}:
            raise ValueError("mode must be one of documents.create|documents.verify|documents.update_status")

        valid_categories = ['verification_id_proof', 'verification_address_proof', 'verification_educational_certificate', 'verification_experience_letter', 'verification_work_visa', 'verification_pr_card', 'verification_bank_proof', 'offer_letter', 'contract', 'policy_acknowledgment', 'tax_form', 'insurance_form', 'nda', 'resume', 'cover_letter', 'job_description', 'budget_justification', 'budget_approval', 'workforce_plan', 'recruitment_checklist', 'promotion_letter', 'transfer_memo', 'other']
        valid_related = ['employee', 'candidate', 'offer', 'onboarding', 'job_requisition', 'job_posting', 'application']

        if mode == "documents.create":
            required = [document_category, related_entity_type, related_entity_id, file_name, file_format, uploaded_by]
            if any(v in (None, "") for v in required):
                raise ValueError("Missing required args for documents.create")
            if document_category not in valid_categories:
                raise ValueError(f"document_category must be one of {valid_categories}")
            if related_entity_type not in valid_related:
                raise ValueError(f"related_entity_type must be one of {valid_related}")

            # naive uniqueness pre-check for file_name (helps fail early in memory-backed envs)
            if any(d.get("file_name")==file_name for d in documents.values()):
                raise ValueError(f"file_name '{file_name}' already exists (must be unique)")

            new_id = str(max([int(k) for k in documents.keys()] + [0]) + 1)
            rec = {
                "document_id": new_id,
                "document_category": document_category,
                "related_entity_type": related_entity_type,
                "related_entity_id": related_entity_id,
                "file_name": file_name,
                "file_format": file_format,
                "upload_date": data.get("_now_utc", "2025-01-01T00:00:00Z"),
                "uploaded_by": uploaded_by,
                "document_status": "active",
                "expiry_date": expiry_date,
                "verification_status": (verification_status or "pending"),
                "created_at": data.get("_now_utc", "2025-01-01T00:00:00Z"),
            }
            documents[new_id] = rec
            return json.dumps(rec)

        if not document_id:
            raise ValueError("document_id is required for verify/update_status")
        if document_id not in documents:
            raise ValueError(f"Document {document_id} not found")

        rec = documents[document_id]
        if mode == "documents.verify":
            if verification_status not in {"pending","verified","failed"}:
                raise ValueError("verification_status must be pending|verified|failed")
            rec["verification_status"] = verification_status
            rec["verified_by"] = data.get("_caller_user_id", "system")
            rec["verified_date"] = (data.get("_now_utc","2025-01-01T00:00:00Z")).split("T")[0]
            return json.dumps(rec)

        if document_status not in {"active","archived","expired"}:
            raise ValueError("document_status must be active|archived|expired")
        rec["document_status"] = document_status
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_document_operations",
                "description": 'Create, verify, or update status of a document with updated category/entity enums.',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "str"},
                        "document_category": {"type": "str"},
                        "related_entity_type": {"type": "str"},
                        "related_entity_id": {"type": "str"},
                        "file_name": {"type": "str"},
                        "file_format": {"type": "str"},
                        "uploaded_by": {"type": "str"},
                        "document_id": {"type": "str"},
                        "expiry_date": {"type": "str"},
                        "verification_status": {"type": "str"},
                        "document_status": {"type": "str"}
                    },
                    "required": ["mode"]
                }
            }
        }

def manage_document_operations(data: Dict[str, Any], **kwargs) -> str:
    return ManageDocumentOperations.invoke(data, **kwargs)
