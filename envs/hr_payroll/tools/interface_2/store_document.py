from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class StoreDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], file: str) -> str:
        doc = data["documents"].get(file)
        if not doc:
            raise ValueError("Document not found.")
        doc["stored_at"] = datetime.utcnow().isoformat()
        return file

    @staticmethod
    def get_info():
        return {
            "name": "store_document",
            "description": "Marks the given document as stored.",
            "parameters": {
                "file": "str"
            },
            "returns": "str"
        }