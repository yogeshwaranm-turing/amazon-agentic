import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageComponents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, component_data: Dict[str, Any] = None, component_id: str = None) -> str:
        """
        Create or update infrastructure component records.
        
        Actions:
        - create: Create new component record (requires component_data with component_name, component_type, environment, status)
        - update: Update existing component record (requires component_id and component_data with changes)
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
        
        # Access infrastructure_components data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for infrastructure_components"
            })
        
        components = data.get("infrastructure_components", {})
        
        if action == "create":
            if not component_data:
                return json.dumps({
                    "success": False,
                    "error": "component_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["component_name", "component_type", "environment", "status"]
            missing_fields = [field for field in required_fields if field not in component_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for component creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["product_id", "component_name", "component_type", "environment", "location", "port_number", "status"]
            invalid_fields = [field for field in component_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for component creation: {', '.join(invalid_fields)}"
                })
            
            # Validate component_type enum
            valid_component_types = ["sftp_server", "api_endpoint", "database", "load_balancer", "firewall", "authentication_service", "payment_gateway", "file_storage", "monitoring_system"]
            if component_data["component_type"] not in valid_component_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid component_type. Must be one of: {', '.join(valid_component_types)}"
                })
            
            # Validate environment enum
            valid_environments = ["production", "staging", "development", "test"]
            if component_data["environment"] not in valid_environments:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid environment. Must be one of: {', '.join(valid_environments)}"
                })
            
            # Validate status enum
            valid_statuses = ["online", "offline", "maintenance", "degraded"]
            if component_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate port_number if provided
            if "port_number" in component_data and component_data["port_number"] is not None:
                try:
                    port = int(component_data["port_number"])
                    if port < 1 or port > 65535:
                        return json.dumps({
                            "success": False,
                            "error": "Port number must be between 1 and 65535"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Port number must be a valid integer"
                    })
            
            # Check for duplicate component name in same environment
            component_name = component_data["component_name"].strip()
            environment = component_data["environment"]
            for existing_component in components.values():
                if (existing_component.get("component_name", "").strip().lower() == component_name.lower() and
                    existing_component.get("environment") == environment):
                    return json.dumps({
                        "success": False,
                        "error": f"Component with name '{component_name}' already exists in {environment} environment"
                    })
            
            # Generate new component ID
            new_component_id = generate_id(components)
            
            # Create new component record
            new_component = {
                "component_id": str(new_component_id),
                "product_id": component_data.get("product_id"),
                "component_name": component_data["component_name"],
                "component_type": component_data["component_type"],
                "environment": component_data["environment"],
                "location": component_data.get("location"),
                "port_number": component_data.get("port_number"),
                "status": component_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            components[str(new_component_id)] = new_component
            return json.dumps(new_component)
        
        elif action == "update":
            if not component_id:
                return json.dumps({
                    "success": False,
                    "error": "component_id is required for update action"
                })
            
            if component_id not in components:
                return json.dumps({
                    "success": False,
                    "error": f"Component {component_id} not found"
                })
            
            if not component_data:
                return json.dumps({
                    "success": False,
                    "error": "component_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["product_id", "component_name", "component_type", "environment", "location", "port_number", "status"]
            invalid_fields = [field for field in component_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for component update: {', '.join(invalid_fields)}"
                })
            
            # Validate component_type enum if provided
            if "component_type" in component_data:
                valid_component_types = ["sftp_server", "api_endpoint", "database", "load_balancer", "firewall", "authentication_service", "payment_gateway", "file_storage", "monitoring_system"]
                if component_data["component_type"] not in valid_component_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid component_type. Must be one of: {', '.join(valid_component_types)}"
                    })
            
            # Validate environment enum if provided
            if "environment" in component_data:
                valid_environments = ["production", "staging", "development", "test"]
                if component_data["environment"] not in valid_environments:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid environment. Must be one of: {', '.join(valid_environments)}"
                    })
            
            # Validate status enum if provided
            if "status" in component_data:
                valid_statuses = ["online", "offline", "maintenance", "degraded"]
                if component_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate port_number if provided
            if "port_number" in component_data and component_data["port_number"] is not None:
                try:
                    port = int(component_data["port_number"])
                    if port < 1 or port > 65535:
                        return json.dumps({
                            "success": False,
                            "error": "Port number must be between 1 and 65535"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Port number must be a valid integer"
                    })
            
            # Get current component for validation
            current_component = components[component_id].copy()
            
            # Check for duplicate component name in same environment if updating name or environment
            if "component_name" in component_data or "environment" in component_data:
                new_component_name = component_data.get("component_name", current_component.get("component_name", "")).strip()
                new_environment = component_data.get("environment", current_component.get("environment"))
                
                for existing_component_id, existing_component in components.items():
                    if (existing_component_id != component_id and
                        existing_component.get("component_name", "").strip().lower() == new_component_name.lower() and
                        existing_component.get("environment") == new_environment):
                        return json.dumps({
                            "success": False,
                            "error": f"Component with name '{new_component_name}' already exists in {new_environment} environment"
                        })
            
            # Update component record
            for key, value in component_data.items():
                current_component[key] = value
            
            current_component["updated_at"] = "2025-10-01T00:00:00"
            components[component_id] = current_component
            
            return json.dumps(current_component)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_components",
                "description": "Create or update infrastructure component records in the incident management system. This tool manages the complete infrastructure component lifecycle including creation of new component records and updates to existing component configurations. For creation, establishes new component records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing component records while maintaining data integrity. Validates component types, environments, prevents duplicate component names within the same environment, and manages component status according to business rules. Essential for infrastructure management, monitoring, and incident tracking operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new component record, 'update' to modify existing component record",
                            "enum": ["create", "update"]
                        },
                        "component_data": {
                            "type": "object",
                            "description": "Component data object. For create: requires component_name (unique per environment), component_type (enum), environment (enum), status (enum), with optional product_id, location, port_number. For update: includes component fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "product_id": {
                                    "type": "string",
                                    "description": "Associated product ID (optional)"
                                },
                                "component_name": {
                                    "type": "string",
                                    "description": "Component name (must be unique within the same environment, required for create)"
                                },
                                "component_type": {
                                    "type": "string",
                                    "description": "Type of infrastructure component (sftp_server, api_endpoint, database, load_balancer, firewall, authentication_service, payment_gateway, file_storage, monitoring_system)",
                                    "enum": ["sftp_server", "api_endpoint", "database", "load_balancer", "firewall", "authentication_service", "payment_gateway", "file_storage", "monitoring_system"]
                                },
                                "environment": {
                                    "type": "string",
                                    "description": "Deployment environment (production, staging, development, test)",
                                    "enum": ["production", "staging", "development", "test"]
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Physical or logical location of the component (optional)"
                                },
                                "port_number": {
                                    "type": "integer",
                                    "description": "Port number if applicable (must be between 1 and 65535, optional)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Component operational status (online, offline, maintenance, degraded)",
                                    "enum": ["online", "offline", "maintenance", "degraded"]
                                }
                            }
                        },
                        "component_id": {
                            "type": "string",
                            "description": "Unique identifier of the component (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
