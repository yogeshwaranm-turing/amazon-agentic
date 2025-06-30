from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid

class GenerateHeatmapDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], risk_groupings: Dict[str, Dict[str, List[str]]]) -> str:
        doc_id = f"heatmap_{uuid.uuid4().hex[:8]}"
        document = {
            "document_id": doc_id,
            "type": "risk_heatmap",
            "content": risk_groupings
        }
        data.setdefault("documents", {})[doc_id] = document
        return doc_id

    @staticmethod
    def get_info():
        return {
            "name": "generate_heatmap_document",
            "description": "Generates a heatmap document for compliance risk groupings.",
            "parameters": {
                "risk_groupings": "Dict[str, Dict[str, List[str]]]"
            },
            "returns": "str"
        }