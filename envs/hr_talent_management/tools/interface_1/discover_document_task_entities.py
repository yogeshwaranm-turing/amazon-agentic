# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DiscoverDocumentTaskEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], mode: str, document_id: str = None, related_entity_type: str = None, related_entity_id: str = None, document_category: str = None, document_status: str = None, verification_status: str = None, task_id: str = None, employee_id: str = None, task_type: str = None, task_status: str = None, limit: int = None, offset: int = None) -> str:
        mode = (mode or "").lower()
        if mode not in {"documents.search","it_tasks.search"}:
            raise ValueError("mode must be documents.search|it_tasks.search")
        limit = int(limit or 50)
        offset = int(offset or 0)

        if mode == "documents.search":
            docs = data.get("documents", {})
            valid_categories = ['verification_id_proof', 'verification_address_proof', 'verification_educational_certificate', 'verification_experience_letter', 'verification_work_visa', 'verification_pr_card', 'verification_bank_proof', 'offer_letter', 'contract', 'policy_acknowledgment', 'tax_form', 'insurance_form', 'nda', 'resume', 'cover_letter', 'job_description', 'budget_justification', 'budget_approval', 'workforce_plan', 'recruitment_checklist', 'promotion_letter', 'transfer_memo', 'other']
            valid_related = ['employee', 'candidate', 'offer', 'onboarding', 'job_requisition', 'job_posting', 'application']
            out = []
            for _, d in docs.items():
                if document_id and d.get("document_id") != document_id: continue
                if related_entity_type and d.get("related_entity_type") != related_entity_type: continue
                if related_entity_id and d.get("related_entity_id") != related_entity_id: continue
                if document_category and d.get("document_category") != document_category: continue
                if document_status and d.get("document_status") != document_status: continue
                if verification_status and d.get("verification_status") != verification_status: continue
                # optional sanity hints (do not block)
                if document_category and document_category not in valid_categories: pass
                if related_entity_type and related_entity_type not in valid_related: pass
                out.append(d)
            return json.dumps({"items": out[offset:offset+limit], "next_offset": offset + min(len(out), limit)})

        tasks = data.get("it_provisioning_tasks", {})
        out = []
        for _, t in tasks.items():
            if task_id and t.get("task_id") != task_id: continue
            if employee_id and t.get("employee_id") != employee_id: continue
            if task_type and t.get("task_type") != task_type: continue
            if task_status and t.get("task_status") != task_status: continue
            out.append(t)
        return json.dumps({"items": out[offset:offset+limit], "next_offset": offset + min(len(out), limit)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_document_task_entities",
                "description": 'Search documents and IT provisioning tasks with updated filters.',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "str"},
                        "document_id": {"type": "str"},
                        "related_entity_type": {"type": "str"},
                        "related_entity_id": {"type": "str"},
                        "document_category": {"type": "str"},
                        "document_status": {"type": "str"},
                        "verification_status": {"type": "str"},
                        "task_id": {"type": "str"},
                        "employee_id": {"type": "str"},
                        "task_type": {"type": "str"},
                        "task_status": {"type": "str"},
                        "limit": {"type": "integer"},
                        "offset": {"type": "integer"}
                    },
                    "required": ["mode"]
                }
            }
        }

def discover_document_task_entities(data: Dict[str, Any], **kwargs) -> str:
    return DiscoverDocumentTaskEntities.invoke(data, **kwargs)
