import json
import time
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ApplyPromoCode(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        promo_code: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]
        flights = data["flights"]

        # Reservation & user validation
        if reservation_id not in reservations:
            return "Error: reservation not found"
          
        res = reservations[reservation_id]

        user_id = res.get("user_id")
        if user_id not in users:
            return "Error: user not found"

        # Recompute total fare from flights.json per cabin
        cabin = res.get("cabin")
        total_fare = 0.0
        for leg in res.get("flights", []):
            fn = leg["flight_number"]
            date = leg["date"]
            
            # Validate flight number and date
            if fn not in flights:
                return f"Error: flight {fn} not found"
            date_info = flights[fn].get("dates", {}).get(date)
            
            # Validate date info and pricing
            if not date_info or "prices" not in date_info:
                return f"Error: pricing unavailable for {fn} on {date}"
              
            # price by cabin
            leg_price = date_info["prices"].get(cabin)
            if leg_price is None:
                return f"Error: no price for cabin {cabin} on {fn} at {date}"
            total_fare += leg_price

        # Validate promo code
        valid_codes: Dict[str, Dict[str, Any]] = {
            "DISCOUNT10": {"type": "percent", "value": 10},
            "FLAT50":     {"type": "flat",    "value": 50},
            "MILES5":     {"type": "percent", "value": 5},
        }
        if promo_code not in valid_codes:
            return json.dumps({"valid": False})

        promo = valid_codes[promo_code]
        # Compute discount
        if promo["type"] == "percent":
            discount = total_fare * promo["value"] / 100
        else:
            discount = promo["value"]

        # Record as a negative payment entry
        timestamp = int(time.time())
        payment_id = f"promo_{promo_code}_{timestamp}"
        entry = {"payment_id": payment_id, "amount": -round(discount, 2)}
        res.setdefault("payment_history", []).append(entry)

        # Return summary
        return json.dumps({
            "reservation_id": reservation_id,
            "promo_code": promo_code,
            "total_fare": round(total_fare, 2),
            "discount_amount": round(discount, 2),
            "amount_due": round(total_fare - discount, 2),
            "payment_history": res["payment_history"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "apply_promo_code",
                "description": (
                    "Validate and apply a promo code: "
                    "recompute fare from flights.json by cabin, "
                    "calculate discount, and append a negative entry to payment_history."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation to discount."
                        },
                        "promo_code": {
                            "type": "string",
                            "description": "One of the valid promo codes."
                        }
                    },
                    "required": ["reservation_id", "promo_code"]
                }
            }
        }

