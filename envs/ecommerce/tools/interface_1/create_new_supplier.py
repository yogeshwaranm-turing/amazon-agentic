import re
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewSupplier(Tool):
    @staticmethod
    def is_valid_email(email: str) -> bool:
        # basic regex for email validation
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        supplier_id: str,
        name: str,
        contact_email: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str
    ) -> str:
        # Check if supplier already exists
        if supplier_id in data.get("suppliers", {}):
            return "Error: supplier already exists"
        # Verify email format
        if not CreateNewSupplier.is_valid_email(contact_email):
            return "Error: invalid email"
        # Create new supplier record
        supplier = {
            "supplier_id": supplier_id,
            "name": name,
            "contact_email": contact_email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country
        }
        # Add supplier to data
        if "suppliers" not in data:
            data["suppliers"] = {}
        data["suppliers"][supplier_id] = supplier
        return json.dumps(supplier)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_supplier",
                "description": "Create a new supplier after verifying supplier data such as email.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {"type": "string", "description": "Unique supplier identifier."},
                        "name": {"type": "string", "description": "Name of the supplier."},
                        "contact_email": {"type": "string", "description": "Contact email of the supplier."},
                        "address": {"type": "string", "description": "Supplier address."},
                        "city": {"type": "string", "description": "City where the supplier is located."},
                        "state": {"type": "string", "description": "State of the supplier."},
                        "zip_code": {"type": "string", "description": "Zip Code."},
                        "country": {"type": "string", "description": "Country of the supplier."}
                    },
                    "required": ["supplier_id", "name", "contact_email", "address", "city", "state", "zip_code", "country"]
                }
            }
        }
