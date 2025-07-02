import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteDisposal(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        disposal_id: str
    ) -> str:
        disposals = data.get("disposals")
        assets = data.get("assets")
        
        if disposal_id not in disposals:
            raise ValueError(f"Disposal {disposal_id} not found.")
          
        disp = disposals.pop(disposal_id)
        aid = disp.get("asset_id")
        
        if aid and aid in assets:
            assets[aid]["status"] = "active"
            assets[aid]["disposal_date"] = None
            assets[aid]["disposal_proceeds"] = None
            
        return json.dumps({"deleted": disposal_id})

    @staticmethod
    def get_info() -> Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"delete_disposal",
                "description":"Undo a disposal and restore the asset.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "disposal_id":{"type":"string"}
                    },
                    "required":["disposal_id"]
                }
            }
        }