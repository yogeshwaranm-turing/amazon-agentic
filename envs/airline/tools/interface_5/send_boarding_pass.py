import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SendBoardingPass(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        email: str,
    ) -> str:
        from get_boarding_pass import GetBoardingPass

        bp_payload = GetBoardingPass.invoke(data, reservation_id)
        
        if bp_payload.startswith("Error"):
            return bp_payload
        
        return json.dumps({
            "status": "sent",
            "to": email,
            "boarding_pass": json.loads(bp_payload)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_boarding_pass",
                "description": "Email the boarding pass to a user’s address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID."
                        },
                        "email": {
                            "type": "string",
                            "description": "Recipient email address."
                        }
                    },
                    "required": ["reservation_id", "email"]
                }
            }
        }