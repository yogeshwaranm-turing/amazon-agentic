import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreatePosition(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        position_id: str,
        title: str,
        department: str,
        location: str,
        employment_type: str
    ) -> str:
        hr_positions = data.setdefault("hr_positions", {})
        if position_id in hr_positions:
            raise ValueError(f"Position ID '{position_id}' already exists.")

        if employment_type not in ["full_time", "part_time", "contract", "intern"]:
            raise ValueError("employment_type must be one of: full_time, part_time, contract, intern")

        position = {
            "position_id": position_id,
            "title": title,
            "department": department,
            "location": location,
            "employment_type": employment_type,
            "created_at": "2025-06-30T09:25:07.697478Z",
            "updated_at": "2025-06-30T09:25:07.697478Z"
        }

        hr_positions[position_id] = position
        return json.dumps(position)

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
                        "position_id": {"type": "string", "description": "Unique ID for the position."},
                        "title": {"type": "string", "description": "Title of the position."},
                        "department": {"type": "string", "description": "Name of the department."},
                        "location": {"type": "string", "description": "Primary location of the job."},
                        "employment_type": {
                            "type": "string",
                            "enum": ["full_time", "part_time", "contract", "intern"],
                            "description": "Type of employment."
                        }
                    },
                    "required": ["position_id", "title", "department", "location", "employment_type"]
                }
            }
        }
