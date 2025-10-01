import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageClientSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, subscription_data: Dict[str, Any] = None, subscription_id: str = None) -> str:
        """
        Create or update client subscription records.
        
        Actions:
        - create: Create new subscription record (requires subscription_data with client_id, product_id, subscription_type, start_date, sla_tier, rto_hours, status)
        - update: Update existing subscription record (requires subscription_id and subscription_data with changes)
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
        
        # Access client_subscriptions data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for client_subscriptions"
            })
        
        subscriptions = data.get("client_subscriptions", {})
        
        if action == "create":
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["client_id", "product_id", "subscription_type", "start_date", "sla_tier", "rto_hours", "status"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["client_id", "product_id", "subscription_type", "start_date", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription creation: {', '.join(invalid_fields)}"
                })
            
            # Validate subscription_type enum
            valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
            if subscription_data["subscription_type"] not in valid_subscription_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid subscription_type. Must be one of: {', '.join(valid_subscription_types)}"
                })
            
            # Validate sla_tier enum
            valid_sla_tiers = ["premium", "standard", "basic"]
            if subscription_data["sla_tier"] not in valid_sla_tiers:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid sla_tier. Must be one of: {', '.join(valid_sla_tiers)}"
                })
            
            # Validate status enum
            valid_statuses = ["active", "expired", "cancelled", "suspended"]
            if subscription_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate rto_hours is positive
            if subscription_data["rto_hours"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "RTO hours must be positive"
                })
            
            # Validate date logic (end_date should be after start_date if provided)
            if "end_date" in subscription_data and subscription_data["end_date"]:
                if subscription_data["end_date"] <= subscription_data["start_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "End date must be after start date"
                    })
            
            # Check for duplicate active subscription for same client-product combination
            client_id = subscription_data["client_id"]
            product_id = subscription_data["product_id"]
            for existing_subscription in subscriptions.values():
                if (existing_subscription.get("client_id") == client_id and
                    existing_subscription.get("product_id") == product_id and
                    existing_subscription.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                    })
            
            # Generate new subscription ID
            new_subscription_id = generate_id(subscriptions)
            
            # Create new subscription record
            new_subscription = {
                "subscription_id": str(new_subscription_id),
                "client_id": subscription_data["client_id"],
                "product_id": subscription_data["product_id"],
                "subscription_type": subscription_data["subscription_type"],
                "start_date": subscription_data["start_date"],
                "end_date": subscription_data.get("end_date"),
                "sla_tier": subscription_data["sla_tier"],
                "rto_hours": subscription_data["rto_hours"],
                "status": subscription_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            subscriptions[str(new_subscription_id)] = new_subscription
            return json.dumps(new_subscription)
        
        elif action == "update":
            if not subscription_id:
                return json.dumps({
                    "success": False,
                    "error": "subscription_id is required for update action"
                })
            
            if subscription_id not in subscriptions:
                return json.dumps({
                    "success": False,
                    "error": f"Subscription {subscription_id} not found"
                })
            
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["subscription_type", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription update: {', '.join(invalid_fields)}. Cannot update client_id, product_id, or start_date."
                })
            
            # Validate subscription_type enum if provided
            if "subscription_type" in subscription_data:
                valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
                if subscription_data["subscription_type"] not in valid_subscription_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid subscription_type. Must be one of: {', '.join(valid_subscription_types)}"
                    })
            
            # Validate sla_tier enum if provided
            if "sla_tier" in subscription_data:
                valid_sla_tiers = ["premium", "standard", "basic"]
                if subscription_data["sla_tier"] not in valid_sla_tiers:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid sla_tier. Must be one of: {', '.join(valid_sla_tiers)}"
                    })
            
            # Validate status enum if provided
            if "status" in subscription_data:
                valid_statuses = ["active", "expired", "cancelled", "suspended"]
                if subscription_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate rto_hours is positive if provided
            if "rto_hours" in subscription_data and subscription_data["rto_hours"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "RTO hours must be positive"
                })
            
            # Get current subscription for validation
            current_subscription = subscriptions[subscription_id].copy()
            
            # Validate date logic if updating end_date
            if "end_date" in subscription_data and subscription_data["end_date"]:
                start_date = current_subscription.get("start_date")
                if subscription_data["end_date"] <= start_date:
                    return json.dumps({
                        "success": False,
                        "error": "End date must be after start date"
                    })
            
            # Check for duplicate active subscription if changing status to active
            if "status" in subscription_data and subscription_data["status"] == "active":
                client_id = current_subscription.get("client_id")
                product_id = current_subscription.get("product_id")
                for existing_subscription_id, existing_subscription in subscriptions.items():
                    if (existing_subscription_id != subscription_id and
                        existing_subscription.get("client_id") == client_id and
                        existing_subscription.get("product_id") == product_id and
                        existing_subscription.get("status") == "active"):
                        return json.dumps({
                            "success": False,
                            "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                        })
            
            # Update subscription record
            for key, value in subscription_data.items():
                current_subscription[key] = value
            
            current_subscription["updated_at"] = "2025-10-01T00:00:00"
            subscriptions[subscription_id] = current_subscription
            
            return json.dumps(current_subscription)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_client_subscriptions",
                "description": "Create or update client subscription records in the incident management system. This tool manages the complete client subscription lifecycle including creation of new subscription records and updates to existing subscription configurations. For creation, establishes new subscription records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing subscription records while maintaining data integrity. Validates subscription types, SLA tiers, prevents duplicate active subscriptions for the same client-product combination, and manages subscription status according to business rules. Essential for subscription management, SLA tracking, and client service level operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new subscription record, 'update' to modify existing subscription record",
                            "enum": ["create", "update"]
                        },
                        "subscription_data": {
                            "type": "object",
                            "description": "Subscription data object. For create: requires client_id, product_id, subscription_type (enum), start_date (YYYY-MM-DD), sla_tier (enum), rto_hours (positive integer), status (enum), with optional end_date (YYYY-MM-DD, must be after start_date). For update: includes subscription fields to change (cannot update client_id, product_id, start_date). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID (required for create, cannot be updated)"
                                },
                                "product_id": {
                                    "type": "string",
                                    "description": "Product ID (required for create, cannot be updated)"
                                },
                                "subscription_type": {
                                    "type": "string",
                                    "description": "Type of subscription (full_service, limited_service, trial, custom)",
                                    "enum": ["full_service", "limited_service", "trial", "custom"]
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Subscription start date in YYYY-MM-DD format (required for create, cannot be updated)"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "Subscription end date in YYYY-MM-DD format (optional, must be after start_date)"
                                },
                                "sla_tier": {
                                    "type": "string",
                                    "description": "SLA tier level (premium, standard, basic)",
                                    "enum": ["premium", "standard", "basic"]
                                },
                                "rto_hours": {
                                    "type": "integer",
                                    "description": "Recovery Time Objective in hours (must be positive)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Subscription status (active, expired, cancelled, suspended)",
                                    "enum": ["active", "expired", "cancelled", "suspended"]
                                }
                            }
                        },
                        "subscription_id": {
                            "type": "string",
                            "description": "Unique identifier of the subscription (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
