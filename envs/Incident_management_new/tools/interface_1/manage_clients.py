import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageClients(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, client_data: Dict[str, Any] = None, client_id: str = None) -> str:
        """
        Create or update client records.
        
        Actions:
        - create: Create new client record (requires client_data with client_name, client_type, status)
        - update: Update existing client record (requires client_id and client_data with changes)
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
        
        # Access clients data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for clients"
            })
        
        clients = data.get("clients", {})
        
        if action == "create":
            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["client_name", "client_type", "status"]
            missing_fields = [field for field in required_fields if field not in client_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for client creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["client_name", "registration_number", "contact_email", "client_type", "industry", "country", "status"]
            invalid_fields = [field for field in client_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for client creation: {', '.join(invalid_fields)}"
                })
            
            # Validate client_type enum
            valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
            if client_data["client_type"] not in valid_client_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                })
            
            # Validate status enum
            valid_statuses = ["active", "inactive", "suspended"]
            if client_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for duplicate client name
            client_name = client_data["client_name"].strip()
            for existing_client in clients.values():
                if existing_client.get("client_name", "").strip().lower() == client_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Client with name '{client_name}' already exists"
                    })
            
            # Generate new client ID
            new_client_id = generate_id(clients)
            
            # Create new client record
            new_client = {
                "client_id": str(new_client_id),
                "client_name": client_data["client_name"],
                "registration_number": client_data.get("registration_number"),
                "contact_email": client_data.get("contact_email"),
                "client_type": client_data["client_type"],
                "industry": client_data.get("industry"),
                "country": client_data.get("country"),
                "status": client_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            clients[str(new_client_id)] = new_client
            return json.dumps(new_client)
        
        elif action == "update":
            if not client_id:
                return json.dumps({
                    "success": False,
                    "error": "client_id is required for update action"
                })
            
            if client_id not in clients:
                return json.dumps({
                    "success": False,
                    "error": f"Client {client_id} not found"
                })
            
            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["client_name", "registration_number", "contact_email", "client_type", "industry", "country", "status"]
            invalid_fields = [field for field in client_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for client update: {', '.join(invalid_fields)}"
                })
            
            # Validate client_type enum if provided
            if "client_type" in client_data:
                valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
                if client_data["client_type"] not in valid_client_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                    })
            
            # Validate status enum if provided
            if "status" in client_data:
                valid_statuses = ["active", "inactive", "suspended"]
                if client_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate client name if updating name
            if "client_name" in client_data:
                new_client_name = client_data["client_name"].strip()
                for existing_client_id, existing_client in clients.items():
                    if (existing_client_id != client_id and 
                        existing_client.get("client_name", "").strip().lower() == new_client_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Client with name '{new_client_name}' already exists"
                        })
            
            # Update client record
            current_client = clients[client_id].copy()
            for key, value in client_data.items():
                current_client[key] = value
            
            current_client["updated_at"] = "2025-10-01T00:00:00"
            clients[client_id] = current_client
            
            return json.dumps(current_client)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_clients",
                "description": "Create or update client records in the incident management system. This tool manages the complete client lifecycle including creation of new client records and updates to existing client configurations. For creation, establishes new client records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing client records while maintaining data integrity. Validates client types, prevents duplicate client names, and manages client status according to business rules. Essential for client management, relationship tracking, and incident assignment operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new client record, 'update' to modify existing client record",
                            "enum": ["create", "update"]
                        },
                        "client_data": {
                            "type": "object",
                            "description": "Client data object. For create: requires client_name (unique), client_type (enum), status (enum), with optional registration_number, contact_email, industry, country. For update: includes client fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "client_name": {
                                    "type": "string",
                                    "description": "Client name (must be unique across all clients, required for create)"
                                },
                                "registration_number": {
                                    "type": "string",
                                    "description": "Client registration number (optional)"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Primary contact email for the client (optional)"
                                },
                                "client_type": {
                                    "type": "string",
                                    "description": "Type of client (enterprise, mid_market, small_business, startup)",
                                    "enum": ["enterprise", "mid_market", "small_business", "startup"]
                                },
                                "industry": {
                                    "type": "string",
                                    "description": "Industry sector of the client (optional)"
                                },
                                "country": {
                                    "type": "string",
                                    "description": "Country where the client is located (optional)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Client operational status (active, inactive, suspended)",
                                    "enum": ["active", "inactive", "suspended"]
                                }
                            }
                        },
                        "client_id": {
                            "type": "string",
                            "description": "Unique identifier of the client (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
