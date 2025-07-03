import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetAvailableFlights(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        origin: str,
        destination: str,
        date: str,
    ) -> str:
        flights = data["flights"]
        results: List[Dict[str, Any]] = []
        
        for fn, f in flights.items():
            if f["origin"] == origin and f["destination"] == destination:
                d = f["dates"].get(date)
                if d and d["status"] == "available":
                    results.append({
                        "flight_number": fn,
                        "origin": f["origin"],
                        "destination": f["destination"],
                        "date": date,
                        "available_seats": d["available_seats"],
                        "prices": d["prices"],
                    })
                    
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_available_flights",
                "description": "Get all available flights between two airports on a specific date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "IATA code of the origin airport."
                        },
                        "destination": {
                            "type": "string",
                            "description": "IATA code of the destination airport."
                        },
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format."
                        }
                    },
                    "required": ["origin", "destination", "date"]
                }
            }
        }