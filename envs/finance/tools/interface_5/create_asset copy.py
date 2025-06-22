import json
from datetime import datetime, timezone
from typing import Any, Dict
from faker import Faker
from tau_bench.envs.tool import Tool

fake = Faker()

class CreateAsset(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        name: str, 
        category: str, 
        purchase_date: str, 
        cost: float, 
        location: str,
        vendor: str,
        user_id: str = "default_user"
    ) -> str:
        assets = data.setdefault("assets", {})
        
        max_id = max([int(aid.split('-')[-1]) for aid in assets] + [1000])
        asset_id = f"AST-{max_id+1:04d}"
        asset = {
            "asset_id": asset_id,
            "name": name,
            "serial_number": f"SN-{fake.bothify(text='?????-#####')}",
            "category": category,
            "description": "",
            "location": location,
            "department": "",
            "purchase_date": purchase_date,
            "vendor": vendor,
            "cost": cost,
            "salvage_value": 0.0,
            "useful_life_years": 0,
            "depreciation_method": "straight_line",
            "warranty_expiration": "",
            "current_book_value": cost,
            "maintenance_schedule": {
                "last_maintenance": purchase_date,
                "next_due": purchase_date
            },
            "status": "active",
            "disposal_date": None,
            "disposal_proceeds": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id
        }
        
        assets[asset_id] = asset
        
        return json.dumps(asset)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"create_asset",
            "description":"Add a new fixed asset to the registry.",
            "parameters":{
                "type":"object",
                "properties":{
                    "name":{"type":"string"},
                    "category":{
                        "type":"string",
                        "enum": ["IT Equipment", "Furniture", "Software", "Vehicle", "Machinery"],
                        "description": "The category of the asset"
                    },
                    "purchase_date":{"type":"string","format":"date"},
                    "cost":{"type":"number"},
                    "location":{"type":"string"},
                    "vendor":{"type":"string"},
                    "user_id":{
                        "type":"string",
                        "description":"The user ID of the customer to whom the asset belongs. Defaults to 'default_user' if not provided."
                    }
                },
                "required":["name","category","purchase_date","cost","location","vendor"]
            }
        }}