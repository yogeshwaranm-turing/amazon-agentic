# request_upgrade.py
# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RequestUpgrade(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        upgrade_to: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        current_cabin = res.get("cabin")
        if current_cabin not in ("basic_economy", "economy", "business"):
            return "Error: invalid current cabin"

        hierarchy = ["basic_economy", "economy", "business"]
        try:
            current_index = hierarchy.index(current_cabin)
        except ValueError:
            return "Error: unrecognized cabin class"

        if upgrade_to not in hierarchy:
            return "Error: invalid target cabin"
        requested_index = hierarchy.index(upgrade_to)

        if requested_index <= current_index:
            return "Error: can only request an upgrade to a higher cabin"
          
        if requested_index == 2 and current_index == 2:
            return "Error: already in the highest cabin (business)"

        return json.dumps({
            "reservation_id": reservation_id,
            "current_cabin": current_cabin,
            "requested_upgrade_to": upgrade_to,
            "eligible": True,
            "message": f"Upgrade request from {current_cabin} to {upgrade_to} is eligible and pending."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "request_upgrade",
                "description": (
                    "Validate and acknowledge an upgrade request if the requested cabin "
                    "is higher than the current cabin on the reservation."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID."
                        },
                        "upgrade_to": {
                            "type": "string",
                            "description": "Desired higher cabin class (basic_economy → economy → business)."
                        }
                    },
                    "required": ["reservation_id", "upgrade_to"]
                }
            }
        }
