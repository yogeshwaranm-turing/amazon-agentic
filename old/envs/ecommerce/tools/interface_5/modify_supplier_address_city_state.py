import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifySupplierAddressCityState(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], supplier_id: str, new_address: Optional[str] = None, new_city: Optional[str] = None, new_state: Optional[str] = None) -> str:
        # Check that suppliers data exists
        if "suppliers" not in data:
            return json.dumps({"error": "suppliers data not provided"})
        # Check that the supplier exists
        if supplier_id not in data["suppliers"]:
            return json.dumps({"error": f"Supplier '{supplier_id}' not found"})
        
        supplier = data["suppliers"][supplier_id]
        # Update fields if new values are provided
        if new_address is not None:
            supplier["address"] = new_address
        if new_city is not None:
            supplier["city"] = new_city
        if new_state is not None:
            supplier["state"] = new_state

        return json.dumps(supplier)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_supplier_address_city_state",
                "description": "Modify the address, city, or state of a supplier.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The ID of the supplier to modify."
                        },
                        "new_address": {
                            "type": "string",
                            "description": "The new address of the supplier.",
                            "default": None
                        },
                        "new_city": {
                            "type": "string",
                            "description": "The new city of the supplier.",
                            "default": None
                        },
                        "new_state": {
                            "type": "string",
                            "description": "The new state of the supplier.",
                            "default": None
                        }
                    },
                    "required": ["supplier_id"]
                }
            }
        }
