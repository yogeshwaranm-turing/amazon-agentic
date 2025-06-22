import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListAirportLounges(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        airport_code: str,
    ) -> str:
        # static data, but uses no other DB
        lounges: List[Dict[str, Any]] = [
            {"airport": "JFK", "lounge": "Admirals Club"},
            {"airport": "JFK", "lounge": "Delta Sky Club"},
            {"airport": "LAX", "lounge": "Star Alliance Lounge"},
            {"airport": "LAX", "lounge": "United Club"},
            {"airport": "ORD", "lounge": "American Admirals Club"},
            {"airport": "ATL", "lounge": "Delta Sky Club"},
            {"airport": "LAG", "lounge": "La Guaira Airport in Venezuela"},
            {"airport": "DFW", "lounge": "Dallas Fort Worth"},
            {"airport": "BOS", "lounge": "Boston Logan International Lounge"},
            {"airport": "DTW", "lounge": "Detroit Metropolitan Airport Lounge"},
            {"airport": "LAS", "lounge": "Las Vegas McCarran International Lounge"},
            {"airport": "LGA", "lounge": "New York LaGuardia Airport Lounge"},
            {"airport": "SFO", "lounge": "San Francisco International Airport Lounge"},
            {"airport": "PHX", "lounge": "Phoenix Sky Harbor International Lounge"},
            {"airport": "SEA", "lounge": "Seattle-Tacoma International Airport Lounge"},
            {"airport": "MIA", "lounge": "Miami International Airport Lounge"},
            {"airport": "EWR", "lounge": "Newark Liberty International Airport Lounge"},
            {"airport": "IAD", "lounge": "Washington Dulles International Airport Lounge"},
            {"airport": "CLT", "lounge": "Charlotte Douglas International Airport Lounge"},
            {"airport": "MCO", "lounge": "Orlando International Airport Lounge"},
            {"airport": "PHL", "lounge": "Philadelphia International Airport Lounge"},
            {"airport": "BWI", "lounge": "Baltimore/Washington International Airport Lounge"},
            {"airport": "HNL", "lounge": "Honolulu International Airport Lounge"},
            {"airport": "TPA", "lounge": "Tampa International Airport Lounge"},
            {"airport": "SAN", "lounge": "San Diego International Airport Lounge"},
            {"airport": "MSP", "lounge": "Minneapolis-Saint Paul International Airport Lounge"},
            {"airport": "STL", "lounge": "St. Louis Lambert International Airport Lounge"},
            {"airport": "BNA", "lounge": "Nashville International Airport Lounge"},
            {"airport": "AUS", "lounge": "Austin-Bergstrom International Airport Lounge"},
            {"airport": "SLC", "lounge": "Salt Lake City International Airport Lounge"},
            {"airport": "CVG", "lounge": "Cincinnati/Northern Kentucky International Airport Lounge"},
            {"airport": "RDU", "lounge": "Raleigh-Durham International Airport Lounge"},
            {"airport": "MCI", "lounge": "Kansas City International Airport Lounge"},
            {"airport": "OAK", "lounge": "Oakland International Airport Lounge"},
            {"airport": "PIT", "lounge": "Pittsburgh International Airport Lounge"},
            {"airport": "SJC", "lounge": "San Jose International Airport Lounge"},
            {"airport": "IND", "lounge": "Indianapolis International Airport Lounge"},
            {"airport": "CMH", "lounge": "John Glenn Columbus International Airport Lounge"},
            {"airport": "CLE", "lounge": "Cleveland Hopkins International Airport Lounge"},
            {"airport": "MKE", "lounge": "General Mitchell International Airport Lounge"},
            {"airport": "BUF", "lounge": "Buffalo Niagara International Airport Lounge"},
            {"airport": "OKC", "lounge": "Will Rogers World Airport Lounge"},
            {"airport": "SDF", "lounge": "Louisville Muhammad Ali International Airport Lounge"},
            {"airport": "MSY", "lounge": "Louis Armstrong New Orleans International Airport Lounge"},
            {"airport": "MEM", "lounge": "Memphis International Airport Lounge"},
            {"airport": "HOU", "lounge": "George Bush Intercontinental Airport Lounge"},
            {"airport": "PVD", "lounge": "T.F. Green Airport Lounge"},
            {"airport": "BHM", "lounge": "Birmingham-Shuttlesworth International Airport Lounge"},
            {"airport": "SAV", "lounge": "Savannah/Hilton Head International Airport Lounge"},
            {"airport": "JAX", "lounge": "Jacksonville International Airport Lounge"},
            {"airport": "FLL", "lounge": "Fort Lauderdale-Hollywood International Airport Lounge"},
            {"airport": "RIC", "lounge": "Richmond International Airport Lounge"},
            {"airport": "TUL", "lounge": "Tulsa International Airport Lounge"},
            {"airport": "OMA", "lounge": "Eppley Airfield Lounge"},
            {"airport": "ABQ", "lounge": "Albuquerque International Sunport Lounge"},
            {"airport": "PDX", "lounge": "Portland International Airport Lounge"},
            {"airport": "BIL", "lounge": "Billings Logan International Airport Lounge"},
            {"airport": "LIT", "lounge": "Bill and Hillary Clinton National Airport Lounge"},
            {"airport": "MSN", "lounge": "Dane County Regional Airport Lounge"},
            {"airport": "GRR", "lounge": "Gerald R. Ford International Airport Lounge"},
            {"airport": "FWA", "lounge": "Fort Wayne International Airport Lounge"},
            {"airport": "MHT", "lounge": "Manchester-Boston Regional Airport Lounge"},
            {"airport": "GSO", "lounge": "Piedmont Triad International Airport Lounge"},
            {"airport": "TYS", "lounge": "McGhee Tyson Airport Lounge"},
            {"airport": "BTR", "lounge": "Baton Rouge Metropolitan Airport Lounge"},
            {"airport": "LBB", "lounge": "Lubbock Preston Smith International Airport Lounge"},
            {"airport": "RNO", "lounge": "Reno-Tahoe International Airport Lounge"},
            {"airport": "COS", "lounge": "Colorado Springs Airport Lounge"},
            {"airport": "GEG", "lounge": "Spokane International Airport Lounge"},
            {"airport": "ICT", "lounge": "Wichita Dwight D. Eisenhower National Airport Lounge"},
            {"airport": "SBA", "lounge": "Santa Barbara Municipal Airport Lounge"},
            {"airport": "MRY", "lounge": "Monterey Peninsula Airport Lounge"},
            {"airport": "BZN", "lounge": "Bozeman Yellowstone International Airport Lounge"},
            {"airport": "FAT", "lounge": "Fresno Yosemite International Airport Lounge"},
            {"airport": "SPS", "lounge": "Wichita Falls Municipal Airport Lounge"},
            {"airport": "LNK", "lounge": "Lincoln Airport Lounge"},
            {"airport": "GJT", "lounge": "Grand Junction Regional Airport Lounge"},
            {"airport": "YUM", "lounge": "Yuma International Airport Lounge"},
            {"airport": "TUS", "lounge": "Tucson International Airport Lounge"},
            {"airport": "ABY", "lounge": "Southwest Georgia Regional Airport Lounge"},
            {"airport": "IAH", "lounge": "Houston George Bush Intercontinental Airport Lounge"},
        ]
        return json.dumps([l for l in lounges if l["airport"] == airport_code])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_airport_lounges",
                "description": "List all lounges at a given airport.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "airport_code": {"type": "string", "description": "IATA code"}
                    },
                    "required": ["airport_code"]
                }
            }
        }