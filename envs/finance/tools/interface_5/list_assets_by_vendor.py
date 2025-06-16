import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListAssetsByVendor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], vendor: str) -> str:
        assets = data.get("assets", {})
        results: List[Dict[str,Any]] = [a for a in assets.values() if a.get("vendor")==vendor]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"list_assets_by_vendor",
            "description":"Filter assets by vendor name.",
            "parameters":{ "type":"object", "properties":{"vendor":{"type":"string"}}, "required":["vendor"]
            }
        }}