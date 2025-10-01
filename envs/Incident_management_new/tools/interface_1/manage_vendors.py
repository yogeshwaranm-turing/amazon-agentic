import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageVendors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, vendor_data: Dict[str, Any] = None, vendor_id: str = None) -> str:
        """
        Create or update vendor records.
        
        Actions:
        - create: Create new vendor record (requires vendor_data with vendor_name, vendor_type, status)
        - update: Update existing vendor record (requires vendor_id and vendor_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access vendors data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for vendors"
            })
        
        vendors = data.get("vendors", {})
        
        if action == "create":
            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["vendor_name", "vendor_type", "status"]
            missing_fields = [field for field in required_fields if field not in vendor_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for vendor creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["vendor_name", "vendor_type", "contact_email", "contact_phone", "status"]
            invalid_fields = [field for field in vendor_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for vendor creation: {', '.join(invalid_fields)}"
                })
            
            # Validate vendor_type enum
            valid_vendor_types = ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
            if vendor_data["vendor_type"] not in valid_vendor_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                })
            
            # Validate status enum
            valid_statuses = ["active", "inactive", "suspended"]
            if vendor_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for duplicate vendor name
            vendor_name = vendor_data["vendor_name"].strip()
            for existing_vendor in vendors.values():
                if existing_vendor.get("vendor_name", "").strip().lower() == vendor_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Vendor with name '{vendor_name}' already exists"
                    })
            
            # Generate new vendor ID
            new_vendor_id = generate_id(vendors)
            
            # Create new vendor record
            new_vendor = {
                "vendor_id": str(new_vendor_id),
                "vendor_name": vendor_data["vendor_name"],
                "vendor_type": vendor_data["vendor_type"],
                "contact_email": vendor_data.get("contact_email"),
                "contact_phone": vendor_data.get("contact_phone"),
                "status": vendor_data["status"],
                "created_at": "2025-10-01T00:00:00"
            }
            
            vendors[str(new_vendor_id)] = new_vendor
            return json.dumps(new_vendor)
        
        elif action == "update":
            if not vendor_id:
                return json.dumps({
                    "success": False,
                    "error": "vendor_id is required for update action"
                })
            
            if vendor_id not in vendors:
                return json.dumps({
                    "success": False,
                    "error": f"Vendor {vendor_id} not found"
                })
            
            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["vendor_name", "vendor_type", "contact_email", "contact_phone", "status"]
            invalid_fields = [field for field in vendor_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for vendor update: {', '.join(invalid_fields)}"
                })
            
            # Validate vendor_type enum if provided
            if "vendor_type" in vendor_data:
                valid_vendor_types = ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
                if vendor_data["vendor_type"] not in valid_vendor_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                    })
            
            # Validate status enum if provided
            if "status" in vendor_data:
                valid_statuses = ["active", "inactive", "suspended"]
                if vendor_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate vendor name if updating name
            if "vendor_name" in vendor_data:
                new_vendor_name = vendor_data["vendor_name"].strip()
                for existing_vendor_id, existing_vendor in vendors.items():
                    if (existing_vendor_id != vendor_id and 
                        existing_vendor.get("vendor_name", "").strip().lower() == new_vendor_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Vendor with name '{new_vendor_name}' already exists"
                        })
            
            # Update vendor record
            current_vendor = vendors[vendor_id].copy()
            for key, value in vendor_data.items():
                current_vendor[key] = value
            
            vendors[vendor_id] = current_vendor
            
            return json.dumps(current_vendor)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_vendors",
                "description": "Create or update vendor records in the incident management system. This tool manages the complete vendor lifecycle including creation of new vendor records and updates to existing vendor configurations. For creation, establishes new vendor records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing vendor records while maintaining data integrity. Validates vendor types, prevents duplicate vendor names, and manages vendor status according to business rules. Essential for vendor management, relationship tracking, and incident escalation operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new vendor record, 'update' to modify existing vendor record",
                            "enum": ["create", "update"]
                        },
                        "vendor_data": {
                            "type": "object",
                            "description": "Vendor data object. For create: requires vendor_name (unique), vendor_type (enum), status (enum), with optional contact_email, contact_phone. For update: includes vendor fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "vendor_name": {
                                    "type": "string",
                                    "description": "Vendor name (must be unique across all vendors, required for create)"
                                },
                                "vendor_type": {
                                    "type": "string",
                                    "description": "Type of vendor (cloud_provider, payment_processor, software_vendor, infrastructure_provider, security_vendor)",
                                    "enum": ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Primary contact email for the vendor (optional)"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Primary contact phone for the vendor (optional)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Vendor operational status (active, inactive, suspended)",
                                    "enum": ["active", "inactive", "suspended"]
                                }
                            }
                        },
                        "vendor_id": {
                            "type": "string",
                            "description": "Unique identifier of the vendor (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
