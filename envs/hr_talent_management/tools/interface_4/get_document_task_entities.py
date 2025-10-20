import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class GetDocumentTaskEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve document and task entities including documents and IT provisioning tasks.

        entity_type: "documents" | "it_provisioning_tasks"
        filters: optional dict with exact-match filtering and date range support
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["documents", "it_provisioning_tasks"]:
            return json.dumps({
                "success": False,
                "error": "Halt: Missing entity_type or invalid entity_type - must be one of: documents, it_provisioning_tasks"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: Discovery tool execution failed due to system errors - invalid data format"
            })
        
        def apply_exact_filters(record: Dict[str, Any], exact_filter_keys: List[str], filters_obj: Dict[str, Any]) -> bool:
            for key in exact_filter_keys:
                if key in filters_obj:
                    if record.get(key) != filters_obj[key]:
                        return False
            return True

        def in_date_range(date_value: Optional[str], start_key: str, end_key: str, filters_obj: Dict[str, Any]) -> bool:
            if not date_value:
                return False if (start_key in filters_obj or end_key in filters_obj) else True
            if start_key in filters_obj and date_value < filters_obj[start_key]:
                return False
            if end_key in filters_obj and date_value > filters_obj[end_key]:
                return False
            return True

        results: List[Dict[str, Any]] = []

        if entity_type == "documents":
            documents = data.get("documents", {})

            # Supported document filters
            document_exact_keys = [
                "document_id", "document_category", "related_entity_type", "related_entity_id", 
                "file_name", "uploaded_by", "document_status", "verification_status", "verified_by"
            ]

            for document_id, document in documents.items():
                record = {**document}

                # Exact-match filters
                if filters:
                    if not apply_exact_filters(record, document_exact_keys, filters):
                        continue

                    # Date range filters for upload_date
                    if not in_date_range(record.get("upload_date"), "upload_date_from", "upload_date_to", filters):
                        continue
                    
                    # Date range filters for expiry_date
                    if not in_date_range(record.get("expiry_date"), "expiry_date_from", "expiry_date_to", filters):
                        continue

                # ensure id present as string
                record["document_id"] = str(document_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "documents",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "it_provisioning_tasks":
            tasks = data.get("it_provisioning_tasks", {})

            # Supported IT task filters
            task_exact_keys = [
                "task_id", "employee_id", "task_type", "assigned_to", "task_status"
            ]

            for task_id, task in tasks.items():
                record = {**task}

                # Exact-match filters
                if filters:
                    if not apply_exact_filters(record, task_exact_keys, filters):
                        continue

                    # Date range filters for completion_date
                    if not in_date_range(record.get("completion_date"), "completion_date_from", "completion_date_to", filters):
                        continue

                # ensure id present as string
                record["task_id"] = str(task_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "it_provisioning_tasks",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        return json.dumps({
            "success": False,
            "error": "Halt: Missing entity_type or invalid entity_type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_document_task_entities",
                "description": "Discover and retrieve document and task entities including documents and IT provisioning tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of document/task entity to discover. Valid values: 'documents', 'it_provisioning_tasks'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For documents: document_id, document_category, related_entity_type, related_entity_id, file_name, upload_date_from, upload_date_to, uploaded_by, document_status, expiry_date_from, expiry_date_to, verification_status, verified_by. For it_provisioning_tasks: task_id, employee_id, task_type, assigned_to, task_status, completion_date_from, completion_date_to"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }