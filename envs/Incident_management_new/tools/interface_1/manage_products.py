import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageProducts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, product_data: Dict[str, Any] = None, product_id: str = None) -> str:
        """
        Create or update product records.
        
        Actions:
        - create: Create new product record (requires product_data with product_name, product_type, status)
        - update: Update existing product record (requires product_id and product_data with changes)
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
        
        # Access products data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for products"
            })
        
        products = data.get("products", {})
        
        if action == "create":
            if not product_data:
                return json.dumps({
                    "success": False,
                    "error": "product_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["product_name", "product_type", "status"]
            missing_fields = [field for field in required_fields if field not in product_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for product creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["product_name", "product_type", "version", "vendor_support_id", "status"]
            invalid_fields = [field for field in product_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for product creation: {', '.join(invalid_fields)}"
                })
            
            # Validate product_type enum
            valid_product_types = ["payment_processing", "banking_system", "api_gateway", "data_integration", "reporting_platform", "security_service", "backup_service", "monitoring_tool"]
            if product_data["product_type"] not in valid_product_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid product_type. Must be one of: {', '.join(valid_product_types)}"
                })
            
            # Validate status enum
            valid_statuses = ["active", "deprecated", "maintenance"]
            if product_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for duplicate product name
            product_name = product_data["product_name"].strip()
            for existing_product in products.values():
                if existing_product.get("product_name", "").strip().lower() == product_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Product with name '{product_name}' already exists"
                    })
            
            # Generate new product ID
            new_product_id = generate_id(products)
            
            # Create new product record
            new_product = {
                "product_id": str(new_product_id),
                "product_name": product_data["product_name"],
                "product_type": product_data["product_type"],
                "version": product_data.get("version"),
                "vendor_support_id": product_data.get("vendor_support_id"),
                "status": product_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            products[str(new_product_id)] = new_product
            return json.dumps(new_product)
        
        elif action == "update":
            if not product_id:
                return json.dumps({
                    "success": False,
                    "error": "product_id is required for update action"
                })
            
            if product_id not in products:
                return json.dumps({
                    "success": False,
                    "error": f"Product {product_id} not found"
                })
            
            if not product_data:
                return json.dumps({
                    "success": False,
                    "error": "product_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["product_name", "product_type", "version", "vendor_support_id", "status"]
            invalid_fields = [field for field in product_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for product update: {', '.join(invalid_fields)}"
                })
            
            # Validate product_type enum if provided
            if "product_type" in product_data:
                valid_product_types = ["payment_processing", "banking_system", "api_gateway", "data_integration", "reporting_platform", "security_service", "backup_service", "monitoring_tool"]
                if product_data["product_type"] not in valid_product_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid product_type. Must be one of: {', '.join(valid_product_types)}"
                    })
            
            # Validate status enum if provided
            if "status" in product_data:
                valid_statuses = ["active", "deprecated", "maintenance"]
                if product_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate product name if updating name
            if "product_name" in product_data:
                new_product_name = product_data["product_name"].strip()
                for existing_product_id, existing_product in products.items():
                    if (existing_product_id != product_id and 
                        existing_product.get("product_name", "").strip().lower() == new_product_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Product with name '{new_product_name}' already exists"
                        })
            
            # Update product record
            current_product = products[product_id].copy()
            for key, value in product_data.items():
                current_product[key] = value
            
            current_product["updated_at"] = "2025-10-01T00:00:00"
            products[product_id] = current_product
            
            return json.dumps(current_product)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_products",
                "description": "Create or update product records in the incident management system. This tool manages the complete product lifecycle including creation of new product records and updates to existing product configurations. For creation, establishes new product records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing product records while maintaining data integrity. Validates product types, prevents duplicate product names, and manages product status according to business rules. Essential for product management, infrastructure tracking, and incident categorization operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new product record, 'update' to modify existing product record",
                            "enum": ["create", "update"]
                        },
                        "product_data": {
                            "type": "object",
                            "description": "Product data object. For create: requires product_name (unique), product_type (enum), status (enum), with optional version, vendor_support_id. For update: includes product fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "product_name": {
                                    "type": "string",
                                    "description": "Product name (must be unique across all products, required for create)"
                                },
                                "product_type": {
                                    "type": "string",
                                    "description": "Type of product (payment_processing, banking_system, api_gateway, data_integration, reporting_platform, security_service, backup_service, monitoring_tool)",
                                    "enum": ["payment_processing", "banking_system", "api_gateway", "data_integration", "reporting_platform", "security_service", "backup_service", "monitoring_tool"]
                                },
                                "version": {
                                    "type": "string",
                                    "description": "Product version (optional)"
                                },
                                "vendor_support_id": {
                                    "type": "string",
                                    "description": "ID of the vendor providing support for this product (optional)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Product operational status (active, deprecated, maintenance)",
                                    "enum": ["active", "deprecated", "maintenance"]
                                }
                            }
                        },
                        "product_id": {
                            "type": "string",
                            "description": "Unique identifier of the product (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
