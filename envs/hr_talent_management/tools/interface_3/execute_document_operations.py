import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ExecuteDocumentOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage document operations including upload, verification, and status updates.
        
        Operations:
        - upload_document: Upload a new document
        - verify_document: Verify a document
        - update_document_status: Update document status
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        valid_operations = ["upload_document", "verify_document", "update_document_status"]
        
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for document operations"
            })
        
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        # UPLOAD DOCUMENT
        if operation_type == "upload_document":
            required_fields = ["document_category", "related_entity_type", "related_entity_id", "file_name", "upload_date", "uploaded_by"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify uploaded_by user exists and is active
            user = users.get(kwargs["uploaded_by"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Uploader not authorized"})
            
            valid_roles = ["hr_recruiter", "hr_admin", "hr_manager", "compliance_officer", "employee"]
            if user.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: Uploader not authorized"})
            
            # Validate file name has valid extension
            file_name = kwargs["file_name"]
            if not file_name or '.' not in file_name:
                return json.dumps({"success": False, "error": "Halt: Invalid file name - must have valid extension"})
            
            # Determine file format from extension
            file_extension = file_name.split('.')[-1].lower()
            valid_extensions = {
                'pdf': 'pdf',
                'doc': 'doc',
                'docx': 'docx',
                'txt': 'txt',
                'jpg': 'jpg',
                'jpeg': 'jpeg',
                'png': 'png',
                'gif': 'gif',
                'xls': 'xls',
                'xlsx': 'xlsx',
                'csv': 'csv'
            }
            
            if file_extension not in valid_extensions:
                return json.dumps({"success": False, "error": "Halt: Invalid file extension - must be one of: pdf, doc, docx, txt, jpg, jpeg, png, gif, xls, xlsx, csv"})
            
            file_format = valid_extensions[file_extension]
            
            # Check for duplicate file name
            for doc in documents.values():
                if doc.get("file_name") == file_name:
                    return json.dumps({"success": False, "error": "Halt: Duplicate document"})
            
            # Create document
            doc_id = generate_id(documents)
            new_document = {
                "document_id": doc_id,
                "document_category": kwargs["document_category"],
                "related_entity_type": kwargs["related_entity_type"],
                "related_entity_id": kwargs["related_entity_id"],
                "file_name": file_name,
                "file_format": file_format,
                "upload_date": kwargs["upload_date"],
                "uploaded_by": kwargs["uploaded_by"],
                "document_status": "active",
                "expiry_date": kwargs.get("expiry_date"),
                "verification_status": "pending",
                "verified_by": None,
                "verified_date": None,
                "created_at": "2025-01-01T12:00:00"
            }
            documents[doc_id] = new_document
            
            return json.dumps({"success": True, "document_id": doc_id, "message": f"Document {doc_id} uploaded successfully"})
        
        # VERIFY DOCUMENT
        elif operation_type == "verify_document":
            required_fields = ["document_id", "verification_status", "verified_by", "verified_date"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            document = documents.get(kwargs["document_id"])
            if not document or document.get("document_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Document not found or not in 'active' status"})
            
            # Verify verifier exists and has appropriate role
            verifier = users.get(kwargs["verified_by"])
            if not verifier or verifier.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Verifier not authorized - user not found or inactive"})
            
            valid_roles = ["compliance_officer", "finance_manager", "hr_manager"]
            if verifier.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: Verifier not authorized"})
            
            # Update verification
            document["verification_status"] = kwargs["verification_status"]
            document["verified_by"] = kwargs["verified_by"]
            document["verified_date"] = kwargs["verified_date"]
            
            return json.dumps({"success": True, "document_id": kwargs["document_id"], "message": f"Document {kwargs['document_id']} verification recorded"})
        
        # UPDATE DOCUMENT STATUS
        elif operation_type == "update_document_status":
            required_fields = ["document_id", "document_status", "user_id"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            document = documents.get(kwargs["document_id"])
            if not document:
                return json.dumps({"success": False, "error": "Halt: Document not found"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            valid_roles = ["hr_admin", "hr_manager", "hr_director"]
            if user.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update status
            document["document_status"] = kwargs["document_status"]
            
            return json.dumps({"success": True, "document_id": kwargs["document_id"], "message": f"Document {kwargs['document_id']} status updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_document_operations",
                "description": "Manage document operations including upload, verification, and status updates in the HR talent management system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation",
                            "enum": ["upload_document", "verify_document", "update_document_status"]
                        },
                        "document_category": {"type": "string", "description": "Document category (required for upload_document)"},
                        "related_entity_type": {"type": "string", "description": "Related entity type (required for upload_document)"},
                        "related_entity_id": {"type": "string", "description": "Related entity ID (required for upload_document)"},
                        "file_name": {"type": "string", "description": "File name with valid extension (required for upload_document, format auto-determined from extension)"},
                        "uploaded_by": {"type": "string", "description": "User ID who uploaded (required for upload_document)"},
                        "upload_date": {"type": "string", "description": "Upload date (required for upload_document)"},
                        "expiry_date": {"type": "string", "description": "Expiry date (optional for upload_document)"},
                        "document_id": {"type": "string", "description": "Document ID (required for verify_document and update_document_status)"},
                        "verification_status": {"type": "string", "description": "Verification status (required for verify_document)"},
                        "verified_by": {"type": "string", "description": "User ID who verified (required for verify_document)"},
                        "verified_date": {"type": "string", "description": "Verification date (required for verify_document)"},
                        "document_status": {"type": "string", "description": "Document status (required for update_document_status)"},
                        "user_id": {"type": "string", "description": "User ID (required for update_document_status)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }
