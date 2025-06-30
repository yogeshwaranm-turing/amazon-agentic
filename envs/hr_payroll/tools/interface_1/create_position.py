import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreatePosition(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        department: str,
        location: str,
        employment_type: str
    ) -> str:
        positions = data.setdefault("hr_positions", {})

        if employment_type not in ["full_time", "part_time", "contract", "intern"]:
            raise ValueError("employment_type must be one of: full_time, part_time, contract, intern")

        # Generate position ID like pos_10000_XX
        base = "pos_10000_"
        suffix = 0
        while f"{base}{suffix}" in positions:
            suffix += 1
        position_id = f"{base}{suffix}"

        now = datetime.now(timezone.utc).isoformat()
        new_position = {
            "title": title,
            "department": department,
            "location": location,
            "employment_type": employment_type,
            "created_at": now,
            "updated_at": now
        }

        positions[position_id] = new_position
        return json.dumps({**new_position, "position_id": position_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_position",
                "description": "Create a new job position for an organization or department.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the position."
                        },
                        "department": {
                            "type": "string",
                            "description": "Name of the department."
                        },
                        "location": {
                            "type": "string",
                            "description": "Primary location of the job."
                        },
                        "employment_type": {
                            "type": "string",
                            "enum": ["full_time", "part_time", "contract", "intern"],
                            "description": "Type of employment."
                        }
                    },
                    "required": ["title", "department", "location", "employment_type"]
                }
            }
        }
