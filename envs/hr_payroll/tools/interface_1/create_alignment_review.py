from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class CreateAlignmentReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        review_id = f"review_{uuid.uuid4().hex[:8]}"
        if "alignment_reviews" not in data:
            data["alignment_reviews"] = {}
        data["alignment_reviews"][review_id] = {
            "review_id": review_id,
            "worker_id": worker_id,
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
        return review_id

    @staticmethod
    def get_info():
        return {
            "name": "create_alignment_review",
            "description": "Creates a review task for misaligned position/department.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }