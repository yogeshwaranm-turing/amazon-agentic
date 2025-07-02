# cancel_upgrade_request.py
# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CancelUpgradeRequest(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        hierarchy = ["basic_economy", "economy", "business"]
        current = res.get("cabin")
        if current not in hierarchy:
            return "Error: invalid cabin class"

        index = hierarchy.index(current)

        if index == 0:
            return "Error: upgrade was never requested"

        new_cabin = hierarchy[index - 1]
        res["cabin"] = new_cabin

        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_upgrade_request",
                "description": (
                    "Revert a reservation’s cabin to the next lower class "
                    "(e.g., business→economy, economy→basic_economy). "
                    "If already in basic_economy, indicates no upgrade existed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID to modify."
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        }

