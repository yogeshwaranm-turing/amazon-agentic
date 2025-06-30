# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.tool import Tool


class TransferToHumanAgent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        summary: str,
    ) -> str:
        return "Transfer to human agent initiated."

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human_agent",
                "description": "Transfer the user to a human agent with a summary of their issue. Only invoke this if the user asks explicitly or the assistant cannot proceed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Summary of the user's request or problem.",
                        },
                    },
                    "required": [
                        "summary",
                    ],
                },
            },
        }
