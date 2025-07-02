import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetFareEstimate(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        origin: str,
        destination: str,
        date: str,
        cabin: str,
    ) -> str:
        flights = data["flights"]
        fares: List[float] = []
        
        for fn, f in flights.items():
            if f["origin"] == origin and f["destination"] == destination:
                d = f["dates"].get(date)
                if d and d["status"] == "available":
                    price = d["prices"].get(cabin)
                    if price is not None:
                        fares.append(price)
                        
        if not fares:
            return "Error: no available flights match criteria"
        
        estimate = min(fares)
        
        return json.dumps({
            "origin": origin,
            "destination": destination,
            "date": date,
            "cabin": cabin,
            "fare_estimate": estimate,
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fare_estimate",
                "description": "Estimate the lowest fare for a given origin, destination, date, and cabin class.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Origin airport IATA code."
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination airport IATA code."
                        },
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format."
                        },
                        "cabin": {
                            "type": "string",
                            "description": "Cabin class (e.g., basic_economy, economy, business)."
                        }
                    },
                    "required": ["origin", "destination", "date", "cabin"]
                }
            }
        }