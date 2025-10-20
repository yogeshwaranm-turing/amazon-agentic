import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class ComputeSchedule(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], calculation_type: str, calculation_data: Dict[str, Any]) -> str:
        """
        Calculate scheduling and timing for routines and operations in the smart home management system.
        Handles next execution calculations, expiration times, date ranges, and staggered routine scheduling.
        """
        
        # Validate calculation_type
        valid_types = ["next_routine_execution", "expiration_datetime", "datetime_range", "staggered_routine"]
        if calculation_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid calculation_type '{calculation_type}'. Must be one of: {', '.join(valid_types)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        if not calculation_data or not isinstance(calculation_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: calculation_data required and must be a dictionary"
            })
        
        # Get routines table from schema
        routines = data.get("routines", {})
        
        # Current datetime reference
        current_datetime = "2025-10-16T14:30:00"
        
        if calculation_type == "next_routine_execution":
            # Calculate next execution time for a routine
            routine_id = calculation_data.get("routine_id")
            
            if not routine_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routine_id required in calculation_data for next_routine_execution"
                })
            
            # Validate routine exists
            if routine_id not in routines:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
                })
            
            routine = routines[routine_id]
            trigger_type = routine.get("trigger_type")
            trigger_value = routine.get("trigger_value")
            schedule_recurrence = routine.get("schedule_recurrence")
            status = routine.get("status")
            
            # Check if routine is enabled
            if status == "disabled":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Routine '{routine_id}' is disabled - cannot calculate next execution"
                })
            
            # Calculate based on trigger type and schedule
            next_execution = None
            calculation_details = {}
            
            if trigger_type == "time":
                # Parse trigger_value as time (HH:MM format)
                if schedule_recurrence == "daily":
                    next_execution = "2025-10-17T" + trigger_value + ":00"
                    calculation_details["recurrence"] = "daily"
                    calculation_details["trigger_time"] = trigger_value
                
                elif schedule_recurrence == "weekdays":
                    next_execution = "2025-10-17T" + trigger_value + ":00"
                    calculation_details["recurrence"] = "weekdays (Mon-Fri)"
                    calculation_details["trigger_time"] = trigger_value
                    calculation_details["note"] = "Next weekday execution"
                
                elif schedule_recurrence == "weekends":
                    next_execution = "2025-10-18T" + trigger_value + ":00"
                    calculation_details["recurrence"] = "weekends (Sat-Sun)"
                    calculation_details["trigger_time"] = trigger_value
                    calculation_details["note"] = "Next weekend execution"
                
                elif schedule_recurrence == "once":
                    next_execution = "2025-10-16T" + trigger_value + ":00"
                    calculation_details["recurrence"] = "once"
                    calculation_details["trigger_time"] = trigger_value
                    calculation_details["note"] = "One-time execution"
                
                else:
                    next_execution = "2025-10-17T" + trigger_value + ":00"
                    calculation_details["recurrence"] = schedule_recurrence
                    calculation_details["trigger_time"] = trigger_value
            
            elif trigger_type == "manual":
                next_execution = None
                calculation_details["note"] = "Manual trigger - no scheduled execution"
            
            elif trigger_type == "location":
                next_execution = None
                calculation_details["note"] = "Location-based trigger - execution depends on geofence events"
            
            elif trigger_type == "sensor":
                next_execution = None
                calculation_details["note"] = "Sensor-based trigger - execution depends on sensor events"
            
            elif trigger_type == "voice":
                next_execution = None
                calculation_details["note"] = "Voice-activated trigger - execution depends on voice commands"
            
            return json.dumps({
                "success": True,
                "calculation_type": "next_routine_execution",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "trigger_type": trigger_type,
                "next_execution": next_execution,
                "calculation_details": calculation_details,
                "message": f"Next execution calculated for routine '{routine.get('routine_name')}'"
            })
        
        elif calculation_type == "expiration_datetime":
            # Calculate expiration datetime by adding duration to current time
            duration_days = calculation_data.get("duration_days")
            
            if duration_days is None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: duration_days required in calculation_data for expiration_datetime"
                })
            
            if not isinstance(duration_days, (int, float)) or duration_days < 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: duration_days must be a non-negative number"
                })
            
            # Parse current datetime
            current_dt = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S")
            
            # Calculate expiration
            expiration_dt = current_dt + timedelta(days=duration_days)
            expiration_datetime_str = expiration_dt.strftime("%Y-%m-%dT%H:%M:%S")
            
            return json.dumps({
                "success": True,
                "calculation_type": "expiration_datetime",
                "current_datetime": current_datetime,
                "duration_days": duration_days,
                "expiration_datetime": expiration_datetime_str,
                "message": f"Expiration datetime calculated: {duration_days} days from current time"
            })
        
        elif calculation_type == "datetime_range":
            # Calculate datetime range (used for queries and analysis)
            start_date = calculation_data.get("start_date")
            end_date = calculation_data.get("end_date")
            
            if start_date and end_date:
                # Validate date format and order
                if len(start_date) == 10:
                    start_date = start_date + "T00:00:00"
                if len(end_date) == 10:
                    end_date = end_date + "T23:59:59"
                
                start_dt = datetime.strptime(start_date[:19], "%Y-%m-%dT%H:%M:%S")
                end_dt = datetime.strptime(end_date[:19], "%Y-%m-%dT%H:%M:%S")
                
                if start_dt > end_dt:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: start_date cannot be after end_date"
                    })
                
                duration_days = (end_dt - start_dt).days
                
                return json.dumps({
                    "success": True,
                    "calculation_type": "datetime_range",
                    "start_datetime": start_date,
                    "end_datetime": end_date,
                    "duration_days": duration_days,
                    "message": f"Datetime range calculated: {duration_days} days"
                })
            
            # Alternative: calculate range from current time
            time_period = calculation_data.get("time_period")
            if time_period:
                current_dt = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S")
                
                if time_period == "last_7_days":
                    start_dt = current_dt - timedelta(days=7)
                    duration_days = 7
                elif time_period == "last_30_days":
                    start_dt = current_dt - timedelta(days=30)
                    duration_days = 30
                elif time_period == "last_90_days":
                    start_dt = current_dt - timedelta(days=90)
                    duration_days = 90
                else:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid time_period '{time_period}'. Must be 'last_7_days', 'last_30_days', or 'last_90_days'"
                    })
                
                start_datetime_str = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
                
                return json.dumps({
                    "success": True,
                    "calculation_type": "datetime_range",
                    "time_period": time_period,
                    "start_datetime": start_datetime_str,
                    "end_datetime": current_datetime,
                    "duration_days": duration_days,
                    "message": f"Datetime range calculated for {time_period}"
                })
            
            return json.dumps({
                "success": False,
                "error": "Halt: Either (start_date and end_date) or time_period required in calculation_data"
            })
        
        elif calculation_type == "staggered_routine":
            # Calculate staggered execution times for multiple routines
            routines_list = calculation_data.get("routines")
            minimum_gap_seconds = calculation_data.get("minimum_gap_seconds", 5)
            
            if not routines_list:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routines list required in calculation_data for staggered_routine"
                })
            
            if not isinstance(routines_list, list) or len(routines_list) < 2:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routines must be a list with at least 2 routine identifiers"
                })
            
            if not isinstance(minimum_gap_seconds, (int, float)) or minimum_gap_seconds < 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: minimum_gap_seconds must be a non-negative number"
                })
            
            # Validate all routines exist and get their current trigger times
            staggered_schedule = []
            base_time = "07:00:00"
            
            for idx, routine_id in enumerate(routines_list):
                if routine_id not in routines:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
                    })
                
                routine = routines[routine_id]
                
                # Calculate staggered time
                offset_seconds = idx * minimum_gap_seconds
                hours = int(base_time[:2])
                minutes = int(base_time[3:5])
                seconds = int(base_time[6:8])
                
                total_seconds = hours * 3600 + minutes * 60 + seconds + offset_seconds
                new_hours = (total_seconds // 3600) % 24
                new_minutes = (total_seconds % 3600) // 60
                new_seconds = total_seconds % 60
                
                new_trigger_time = f"{new_hours:02d}:{new_minutes:02d}:{new_seconds:02d}"
                
                staggered_schedule.append({
                    "routine_id": routine_id,
                    "routine_name": routine.get("routine_name"),
                    "original_trigger_time": routine.get("trigger_value"),
                    "new_trigger_time": new_trigger_time,
                    "offset_seconds": offset_seconds
                })
            
            return json.dumps({
                "success": True,
                "calculation_type": "staggered_routine",
                "minimum_gap_seconds": minimum_gap_seconds,
                "total_routines": len(routines_list),
                "staggered_schedule": staggered_schedule,
                "message": f"Staggered schedule calculated for {len(routines_list)} routines with {minimum_gap_seconds}s gaps"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "compute_schedule",
                "description": "Calculate scheduling and timing for routines and operations in the smart home management system. Supports next execution time calculation based on trigger type and recurrence, expiration datetime calculation for guest access and time-bound operations, datetime range calculation for queries and analysis, and staggered routine scheduling to prevent device conflicts. Essential for SOPs involving routine creation, guest access management, activity analysis, and conflict resolution.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calculation_type": {
                            "type": "string",
                            "description": "Type of scheduling calculation to perform",
                            "enum": ["next_routine_execution", "expiration_datetime", "datetime_range", "staggered_routine"]
                        },
                        "calculation_data": {
                            "type": "object",
                            "description": "Calculation parameters based on calculation_type. For next_routine_execution: {routine_id}. For expiration_datetime: {duration_days}. For datetime_range: {start_date, end_date} or {time_period}. For staggered_routine: {routines[], minimum_gap_seconds}",
                            "properties": {
                                "routine_id": {
                                    "type": "string",
                                    "description": "Routine identifier (for next_routine_execution)"
                                },
                                "duration_days": {
                                    "type": "number",
                                    "description": "Number of days to add (for expiration_datetime)"
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Start date in YYYY-MM-DD format (for datetime_range)"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "End date in YYYY-MM-DD format (for datetime_range)"
                                },
                                "time_period": {
                                    "type": "string",
                                    "description": "Predefined time period: last_7_days, last_30_days, last_90_days (for datetime_range)"
                                },
                                "routines": {
                                    "type": "array",
                                    "description": "List of routine IDs to stagger (for staggered_routine)",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "minimum_gap_seconds": {
                                    "type": "number",
                                    "description": "Minimum gap in seconds between staggered routines (default: 5)"
                                }
                            }
                        }
                    },
                    "required": ["calculation_type", "calculation_data"]
                }
            }
        }