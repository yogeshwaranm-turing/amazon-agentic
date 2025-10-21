import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class ConfirmSystemState(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        verification_type: str,
        verification_data: Dict[str, Any],
        entity_id: Optional[str] = None
    ) -> str:
        """
        Verify system states, prerequisites, and requirements.
        
        Supported verification types:
        - device_action: Verify device supports a specific action
        - device_echo: Verify if device is an Echo device
        - device_privacy_capabilities: Verify device supports privacy controls
        - device_network_compatibility: Verify device network compatibility
        - skill_compatibility: Verify skill compatibility with system
        - update_prerequisites: Verify device meets firmware update prerequisites
        - pin_configured: Verify PIN is configured for security
        - storage_accessible: Verify storage (cloud/local) is accessible
        - storage_space: Verify sufficient storage space available
        - backup_file_exists: Verify backup file exists
        - backup_checksum: Verify backup file integrity via checksum
        - firmware_version: Verify device firmware version
        - interior_sensors_disarmed: Verify interior motion sensors are disarmed
        - announcement_playback: Verify announcement played correctly
        - security_actions_present: Verify security actions are present
        - perimeter_actions_present: Verify perimeter security actions are present
        - no_interior_sensors_armed: Verify no interior sensors are armed
        - armed_stay_requirements: Verify Armed Stay scene requirements
        - disarm_requirements: Verify Disarm scene requirements
        - disarm_actions_present: Verify disarm actions are present
        - routine_has_awareness_actions: Verify routine contains awareness actions
        - geofence_parameters: Verify geofence parameters are valid
        - critical_routines_scheduled: Verify if critical routines are scheduled
        - energy_monitoring_support: Verify device supports energy monitoring
        - device_capability: Verify device has specific capability
        - voice_profile_quality: Verify voice profile quality meets threshold
        - voice_profile_status: Verify voice profile status
        - routine_trigger_valid: Verify routine trigger configuration is valid
        - device_type_benchmarks: Verify device meets type-specific benchmarks
        - network_bandwidth: Verify network bandwidth meets requirements
        """
        
        VALID_VERIFICATION_TYPES = [
            "device_action", "device_echo", "device_privacy_capabilities",
            "device_network_compatibility", "skill_compatibility", "update_prerequisites",
            "pin_configured", "storage_accessible", "storage_space", "backup_file_exists",
            "backup_checksum", "firmware_version", "interior_sensors_disarmed",
            "announcement_playback", "security_actions_present", "perimeter_actions_present",
            "no_interior_sensors_armed", "armed_stay_requirements", "disarm_requirements",
            "disarm_actions_present", "routine_has_awareness_actions", "geofence_parameters",
            "critical_routines_scheduled", "energy_monitoring_support", "device_capability",
            "voice_profile_quality", "voice_profile_status", "routine_trigger_valid",
            "device_type_benchmarks", "network_bandwidth"
        ]
        
        if verification_type not in VALID_VERIFICATION_TYPES:
            return json.dumps({
                "success": False,
                "error": f"Invalid verification_type '{verification_type}'. Must be one of: {', '.join(VALID_VERIFICATION_TYPES)}"
            })
        
        if not isinstance(verification_data, dict):
            return json.dumps({
                "success": False,
                "error": "verification_data must be a JSON object"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # Validate verification_data has required fields for verification_type
        validation_error = ConfirmSystemState._validate_verification_data(verification_type, verification_data, entity_id)
        if validation_error:
            return json.dumps({
                "success": False,
                "error": validation_error
            })

        # Route to appropriate verification handler
        try:
            if verification_type == "device_action":
                return ConfirmSystemState._verify_device_action(data, verification_data)
            
            elif verification_type == "device_echo":
                return ConfirmSystemState._verify_device_echo(data, entity_id or verification_data.get("device_id"))
            
            elif verification_type == "device_privacy_capabilities":
                return ConfirmSystemState._verify_device_privacy_capabilities(data, entity_id or verification_data.get("device_id"), verification_data)
            
            elif verification_type == "device_network_compatibility":
                return ConfirmSystemState._verify_device_network_compatibility(data, verification_data)
            
            elif verification_type == "skill_compatibility":
                return ConfirmSystemState._verify_skill_compatibility(data, verification_data)
            
            elif verification_type == "update_prerequisites":
                return ConfirmSystemState._verify_update_prerequisites(data, entity_id or verification_data.get("device_id"))
            
            elif verification_type == "pin_configured":
                return ConfirmSystemState._verify_pin_configured(data, verification_data)
            
            elif verification_type == "storage_accessible":
                return ConfirmSystemState._verify_storage_accessible(data, verification_data)
            
            elif verification_type == "storage_space":
                return ConfirmSystemState._verify_storage_space(data, verification_data)
            
            elif verification_type == "backup_file_exists":
                return ConfirmSystemState._verify_backup_file_exists(data, verification_data)
            
            elif verification_type == "backup_checksum":
                return ConfirmSystemState._verify_backup_checksum(data, verification_data)
            
            elif verification_type == "firmware_version":
                return ConfirmSystemState._verify_firmware_version(data, entity_id or verification_data.get("device_id"), verification_data)
            
            elif verification_type == "interior_sensors_disarmed":
                return ConfirmSystemState._verify_interior_sensors_disarmed(data, verification_data)
            
            elif verification_type == "announcement_playback":
                return ConfirmSystemState._verify_announcement_playback(data, verification_data)
            
            elif verification_type == "security_actions_present":
                return ConfirmSystemState._verify_security_actions_present(data, verification_data)
            
            elif verification_type == "perimeter_actions_present":
                return ConfirmSystemState._verify_perimeter_actions_present(data, verification_data)
            
            elif verification_type == "no_interior_sensors_armed":
                return ConfirmSystemState._verify_no_interior_sensors_armed(data, verification_data)
            
            elif verification_type == "armed_stay_requirements":
                return ConfirmSystemState._verify_armed_stay_requirements(data, verification_data)
            
            elif verification_type == "disarm_requirements":
                return ConfirmSystemState._verify_disarm_requirements(data, verification_data)
            
            elif verification_type == "disarm_actions_present":
                return ConfirmSystemState._verify_disarm_actions_present(data, verification_data)
            
            elif verification_type == "routine_has_awareness_actions":
                return ConfirmSystemState._verify_routine_has_awareness_actions(data, verification_data)
            
            elif verification_type == "geofence_parameters":
                return ConfirmSystemState._verify_geofence_parameters(data, verification_data)
            
            elif verification_type == "critical_routines_scheduled":
                return ConfirmSystemState._verify_critical_routines_scheduled(data, verification_data)
            
            elif verification_type == "energy_monitoring_support":
                return ConfirmSystemState._verify_energy_monitoring_support(data, entity_id or verification_data.get("device_id"))
            
            elif verification_type == "device_capability":
                return ConfirmSystemState._verify_device_capability(data, verification_data)
            
            elif verification_type == "voice_profile_quality":
                return ConfirmSystemState._verify_voice_profile_quality(data, verification_data)
            
            elif verification_type == "voice_profile_status":
                return ConfirmSystemState._verify_voice_profile_status(data, verification_data)
            
            elif verification_type == "routine_trigger_valid":
                return ConfirmSystemState._verify_routine_trigger_valid(data, verification_data)
            
            elif verification_type == "device_type_benchmarks":
                return ConfirmSystemState._verify_device_type_benchmarks(data, verification_data)
            
            elif verification_type == "network_bandwidth":
                return ConfirmSystemState._verify_network_bandwidth(data, verification_data)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Verification failed: {str(e)}"
            })
    
    @staticmethod
    def _validate_verification_data(verification_type: str, verification_data: Dict[str, Any], entity_id: Optional[str]) -> Optional[str]:
        """
        Validate that verification_data contains required fields for the verification type.

        Returns:
            Error message if validation fails, None if validation passes.
        """
        # Define required fields for each verification type
        required_fields = {
            "device_action": ["device_id", "action"],
            "device_echo": [],  # device_id can come from entity_id
            "device_privacy_capabilities": ["requested_settings"],
            "device_network_compatibility": ["device_id", "network_frequency"],
            "skill_compatibility": ["skill_id"],
            "update_prerequisites": [],  # device_id can come from entity_id
            "storage_accessible": ["storage_type"],
            "storage_space": ["required_space_mb"],
            "backup_file_exists": ["backup_id"],
            "backup_checksum": ["backup_id", "expected_checksum"],
            "firmware_version": ["expected_version"],
            "interior_sensors_disarmed": ["routine_id"],
            "announcement_playback": ["routine_id"],
            "security_actions_present": ["security_actions"],
            "perimeter_actions_present": ["security_actions"],
            "no_interior_sensors_armed": ["security_actions"],
            "armed_stay_requirements": ["security_actions"],
            "disarm_requirements": ["disarm_actions", "voice_trigger"],
            "disarm_actions_present": ["disarm_actions"],
            "routine_has_awareness_actions": ["routine_id"],
            "geofence_parameters": ["latitude", "longitude", "radius_meters"],
            "device_capability": ["device_id", "capability"],
            "voice_profile_quality": ["user_id", "min_quality_threshold"],
            "voice_profile_status": ["user_id", "expected_status"],
            "routine_trigger_valid": ["trigger_type"],
            "device_type_benchmarks": ["device_id"],
            "network_bandwidth": ["required_bandwidth_mbps"]
        }

        fields = required_fields.get(verification_type, [])

        for field in fields:
            if field not in verification_data and field != "device_id":
                return f"Missing required field '{field}' in verification_data for verification_type '{verification_type}'"

            # Special handling for device_id which can come from entity_id
            if field == "device_id" and "device_id" not in verification_data and not entity_id:
                return f"Missing required field 'device_id' (must be in verification_data or entity_id parameter)"

        # Type-specific validation
        if verification_type == "storage_accessible":
            storage_type = verification_data.get("storage_type")
            if storage_type not in ["cloud", "local"]:
                return f"Invalid storage_type '{storage_type}'. Must be 'cloud' or 'local'"

        if verification_type == "geofence_parameters":
            latitude = verification_data.get("latitude")
            longitude = verification_data.get("longitude")
            radius_meters = verification_data.get("radius_meters")

            if not isinstance(latitude, (int, float)):
                return "latitude must be a numeric value"
            if not isinstance(longitude, (int, float)):
                return "longitude must be a numeric value"
            if not isinstance(radius_meters, (int, float)):
                return "radius_meters must be a numeric value"

        if verification_type == "voice_profile_quality":
            threshold = verification_data.get("min_quality_threshold")
            if threshold is not None and not isinstance(threshold, (int, float)):
                return "min_quality_threshold must be a numeric value"

        if verification_type == "network_bandwidth":
            bandwidth = verification_data.get("required_bandwidth_mbps")
            if not isinstance(bandwidth, (int, float)):
                return "required_bandwidth_mbps must be a numeric value"

        if verification_type == "storage_space":
            space = verification_data.get("required_space_mb")
            if not isinstance(space, (int, float)):
                return "required_space_mb must be a numeric value"

        return None

    # ==================== Verification Handler Methods ====================
    
    @staticmethod
    def _verify_device_action(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify device supports a specific action"""
        device_id = verification_data.get("device_id")
        action = verification_data.get("action")
        
        if not device_id or not action:
            return json.dumps({
                "success": False,
                "error": "device_id and action are required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        device_type = device.get("device_type")
        supported_actions = device.get("supported_actions", [])
        
        action_supported = action in supported_actions
        
        return json.dumps({
            "success": True,
            "verified": action_supported,
            "device_id": device_id,
            "device_type": device_type,
            "action": action,
            "supported": action_supported
        })
    
    @staticmethod
    def _verify_device_echo(data: Dict[str, Any], device_id: Optional[str]) -> str:
        """Verify if device is an Echo device"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        device_type = device.get("device_type", "")
        manufacturer = device.get("manufacturer", "")
        
        is_echo = (manufacturer.lower() == "amazon" and 
                   "echo" in device_type.lower())
        
        return json.dumps({
            "success": True,
            "verified": is_echo,
            "device_id": device_id,
            "is_echo_device": is_echo,
            "device_type": device_type,
            "manufacturer": manufacturer
        })
    
    @staticmethod
    def _verify_device_privacy_capabilities(data: Dict[str, Any], device_id: Optional[str], verification_data: Dict[str, Any]) -> str:
        """Verify device supports requested privacy controls"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        privacy_capabilities = device.get("privacy_capabilities", [])
        requested_settings = verification_data.get("requested_settings", {})
        
        all_supported = True
        unsupported_settings = []
        
        for setting_name in requested_settings.keys():
            capability_name = f"{setting_name}_control"
            if capability_name not in privacy_capabilities:
                all_supported = False
                unsupported_settings.append(setting_name)
        
        return json.dumps({
            "success": True,
            "verified": all_supported,
            "device_id": device_id,
            "supported": all_supported,
            "capabilities": privacy_capabilities,
            "unsupported_settings": unsupported_settings if unsupported_settings else None
        })
    
    @staticmethod
    def _verify_device_network_compatibility(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify device network compatibility"""
        device_id = verification_data.get("device_id")
        network_frequency = verification_data.get("network_frequency")
        
        if not device_id or not network_frequency:
            return json.dumps({
                "success": False,
                "error": "device_id and network_frequency are required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        supported_frequencies = device.get("supported_frequencies", [])
        compatible = network_frequency in supported_frequencies
        
        return json.dumps({
            "success": True,
            "verified": compatible,
            "device_id": device_id,
            "network_frequency": network_frequency,
            "compatible": compatible,
            "supported_frequencies": supported_frequencies
        })
    
    @staticmethod
    def _verify_skill_compatibility(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify skill compatibility with system"""
        skill_id = verification_data.get("skill_id")
        
        if not skill_id:
            return json.dumps({
                "success": False,
                "error": "skill_id is required"
            })
        
        skills = data.get("skills", {})
        skill = skills.get(skill_id)
        
        if not skill:
            return json.dumps({
                "success": False,
                "error": f"Skill {skill_id} not found"
            })
        
        compatibility_status = skill.get("compatibility_status", "unknown")
        compatible = compatibility_status == "compatible"
        
        return json.dumps({
            "success": True,
            "verified": compatible,
            "skill_id": skill_id,
            "compatible": compatible,
            "compatibility_status": compatibility_status
        })
    
    @staticmethod
    def _verify_update_prerequisites(data: Dict[str, Any], device_id: Optional[str]) -> str:
        """Verify device meets firmware update prerequisites"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        connection_status = device.get("connection_status")
        battery_level = device.get("battery_level")
        signal_strength = device.get("signal_strength")
        power_source = device.get("power_source", "battery")
        
        # Prerequisites: online, battery >20% (or plugged in), signal >-70 dBm
        prerequisites_met = (
            connection_status == "online" and
            (power_source == "plugged_in" or (battery_level is not None and battery_level > 20)) and
            (signal_strength is not None and signal_strength > -70)
        )
        
        return json.dumps({
            "success": True,
            "verified": prerequisites_met,
            "device_id": device_id,
            "prerequisites_met": prerequisites_met,
            "connection_status": connection_status,
            "battery_level": battery_level,
            "signal_strength": signal_strength,
            "power_source": power_source,
            "ready_for_update": prerequisites_met
        })
    
    @staticmethod
    def _verify_pin_configured(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify PIN is configured for security"""
        user_id = verification_data.get("user_id")
        
        security_settings = data.get("security_settings", {})
        pin_configured = security_settings.get("pin_configured", False)
        
        return json.dumps({
            "success": True,
            "verified": pin_configured,
            "pin_configured": pin_configured
        })
    
    @staticmethod
    def _verify_storage_accessible(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify storage (cloud/local) is accessible"""
        storage_type = verification_data.get("storage_type")
        
        if not storage_type:
            return json.dumps({
                "success": False,
                "error": "storage_type is required (cloud or local)"
            })
        
        storage_status = data.get("storage_status", {})
        accessible = storage_status.get(f"{storage_type}_accessible", False)
        
        return json.dumps({
            "success": True,
            "verified": accessible,
            "storage_type": storage_type,
            "accessible": accessible
        })
    
    @staticmethod
    def _verify_storage_space(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify sufficient storage space available"""
        required_space_mb = verification_data.get("required_space_mb")
        
        if required_space_mb is None:
            return json.dumps({
                "success": False,
                "error": "required_space_mb is required"
            })
        
        storage_status = data.get("storage_status", {})
        available_space_mb = storage_status.get("available_space_mb", 0)
        
        sufficient = available_space_mb >= required_space_mb
        
        return json.dumps({
            "success": True,
            "verified": sufficient,
            "sufficient_space": sufficient,
            "available_space_mb": available_space_mb,
            "required_space_mb": required_space_mb
        })
    
    @staticmethod
    def _verify_backup_file_exists(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify backup file exists"""
        backup_id = verification_data.get("backup_id")
        
        if not backup_id:
            return json.dumps({
                "success": False,
                "error": "backup_id is required"
            })
        
        backups = data.get("backups", {})
        backup_exists = backup_id in backups
        
        return json.dumps({
            "success": True,
            "verified": backup_exists,
            "backup_id": backup_id,
            "exists": backup_exists
        })
    
    @staticmethod
    def _verify_backup_checksum(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify backup file integrity via checksum"""
        backup_id = verification_data.get("backup_id")
        expected_checksum = verification_data.get("expected_checksum")
        
        if not backup_id or not expected_checksum:
            return json.dumps({
                "success": False,
                "error": "backup_id and expected_checksum are required"
            })
        
        backups = data.get("backups", {})
        backup = backups.get(backup_id, {})
        actual_checksum = backup.get("checksum")
        
        checksum_valid = actual_checksum == expected_checksum
        
        return json.dumps({
            "success": True,
            "verified": checksum_valid,
            "backup_id": backup_id,
            "checksum_valid": checksum_valid,
            "integrity_verified": checksum_valid
        })
    
    @staticmethod
    def _verify_firmware_version(data: Dict[str, Any], device_id: Optional[str], verification_data: Dict[str, Any]) -> str:
        """Verify device firmware version"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        expected_version = verification_data.get("expected_version")
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        current_version = device.get("firmware_version")
        version_match = current_version == expected_version
        
        return json.dumps({
            "success": True,
            "verified": version_match,
            "device_id": device_id,
            "current_version": current_version,
            "expected_version": expected_version,
            "update_successful": version_match
        })
    
    @staticmethod
    def _verify_interior_sensors_disarmed(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify interior motion sensors are disarmed"""
        routine_id = verification_data.get("routine_id")
        
        if not routine_id:
            return json.dumps({
                "success": False,
                "error": "routine_id is required"
            })
        
        routines = data.get("routines", {})
        routine = routines.get(routine_id, {})
        device_actions = routine.get("device_actions", [])
        
        interior_sensors_armed = False
        for action in device_actions:
            device_id = action.get("device_id")
            action_type = action.get("action")
            
            devices = data.get("devices", {})
            device = devices.get(device_id, {})
            
            if (device.get("device_type") == "sensor" and
                device.get("sensor_type") == "motion" and
                device.get("location_type") == "interior" and
                action_type == "arm"):
                interior_sensors_armed = True
                break
        
        return json.dumps({
            "success": True,
            "verified": not interior_sensors_armed,
            "routine_id": routine_id,
            "interior_sensors_disarmed": not interior_sensors_armed
        })
    
    @staticmethod
    def _verify_announcement_playback(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify announcement played correctly"""
        routine_id = verification_data.get("routine_id")
        
        if not routine_id:
            return json.dumps({
                "success": False,
                "error": "routine_id is required"
            })
        
        routine_executions = data.get("routine_executions", {})
        execution = routine_executions.get(routine_id, {})
        announcement_status = execution.get("announcement_playback_status", "unknown")
        
        played_correctly = announcement_status == "success"
        
        return json.dumps({
            "success": True,
            "verified": played_correctly,
            "routine_id": routine_id,
            "announcement_played_correctly": played_correctly,
            "playback_status": announcement_status
        })
    
    @staticmethod
    def _verify_security_actions_present(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify security actions are present"""
        security_actions = verification_data.get("security_actions", [])
        
        valid_security_actions = ["arm_system", "lock_door", "activate_camera"]
        has_security_action = any(
            action.get("action") in valid_security_actions
            for action in security_actions
        )
        
        return json.dumps({
            "success": True,
            "verified": has_security_action,
            "security_actions_present": has_security_action
        })
    
    @staticmethod
    def _verify_perimeter_actions_present(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify perimeter security actions are present"""
        security_actions = verification_data.get("security_actions", [])
        
        valid_perimeter_actions = ["arm_perimeter", "lock_exterior_door", "activate_exterior_camera"]
        has_perimeter_action = any(
            action.get("action") in valid_perimeter_actions
            for action in security_actions
        )
        
        return json.dumps({
            "success": True,
            "verified": has_perimeter_action,
            "perimeter_actions_present": has_perimeter_action
        })
    
    @staticmethod
    def _verify_no_interior_sensors_armed(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify no interior sensors are armed"""
        security_actions = verification_data.get("security_actions", [])
        
        devices = data.get("devices", {})
        
        interior_sensors_armed = False
        for action in security_actions:
            device_id = action.get("device_id")
            action_type = action.get("action")
            
            device = devices.get(device_id, {})
            if (device.get("device_type") == "sensor" and
                device.get("sensor_type") == "motion" and
                device.get("location_type") == "interior" and
                action_type == "arm"):
                interior_sensors_armed = True
                break
        
        return json.dumps({
            "success": True,
            "verified": not interior_sensors_armed,
            "no_interior_sensors_armed": not interior_sensors_armed
        })
    
    @staticmethod
    def _verify_armed_stay_requirements(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify Armed Stay scene requirements"""
        security_actions = verification_data.get("security_actions", [])
        
        # Check for perimeter actions
        perimeter_result = json.loads(
            ConfirmSystemState._verify_perimeter_actions_present(data, verification_data)
        )
        has_perimeter = perimeter_result.get("perimeter_actions_present", False)
        
        # Check no interior sensors armed
        interior_result = json.loads(
            ConfirmSystemState._verify_no_interior_sensors_armed(data, verification_data)
        )
        no_interior = interior_result.get("no_interior_sensors_armed", False)
        
        requirements_met = has_perimeter and no_interior
        
        return json.dumps({
            "success": True,
            "verified": requirements_met,
            "armed_stay_requirements_met": requirements_met,
            "has_perimeter_actions": has_perimeter,
            "no_interior_sensors_armed": no_interior
        })
    
    @staticmethod
    def _verify_disarm_requirements(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify Disarm scene requirements"""
        disarm_actions = verification_data.get("disarm_actions", [])
        voice_trigger = verification_data.get("voice_trigger", False)
        
        has_disarm_action = any(
            action.get("action") in ["disarm_system", "unlock_door", "deactivate_camera"]
            for action in disarm_actions
        )
        
        security_settings = data.get("security_settings", {})
        pin_configured = security_settings.get("pin_configured", False)
        
        requirements_met = has_disarm_action and (not voice_trigger or pin_configured)
        
        return json.dumps({
            "success": True,
            "verified": requirements_met,
            "disarm_requirements_met": requirements_met,
            "has_disarm_actions": has_disarm_action,
            "pin_configured": pin_configured if voice_trigger else None
        })
    
    @staticmethod
    def _verify_disarm_actions_present(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify disarm actions are present"""
        disarm_actions = verification_data.get("disarm_actions", [])
        
        valid_disarm_actions = ["disarm_system", "unlock_door", "deactivate_camera"]
        has_disarm_action = any(
            action.get("action") in valid_disarm_actions
            for action in disarm_actions
        )
        
        return json.dumps({
            "success": True,
            "verified": has_disarm_action,
            "disarm_actions_present": has_disarm_action
        })
    
    @staticmethod
    def _verify_routine_has_awareness_actions(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify routine contains awareness actions"""
        routine_id = verification_data.get("routine_id")
        
        if not routine_id:
            return json.dumps({
                "success": False,
                "error": "routine_id is required"
            })
        
        routines = data.get("routines", {})
        routine = routines.get(routine_id, {})
        device_actions = routine.get("device_actions", [])
        
        awareness_actions = ["notification", "reminder", "alert", "announcement"]
        has_awareness = any(
            action.get("action") in awareness_actions
            for action in device_actions
        )
        
        return json.dumps({
            "success": True,
            "verified": has_awareness,
            "routine_id": routine_id,
            "has_awareness_actions": has_awareness
        })
    
    @staticmethod
    def _verify_geofence_parameters(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify geofence parameters are valid"""
        latitude = verification_data.get("latitude")
        longitude = verification_data.get("longitude")
        radius_meters = verification_data.get("radius_meters")
        
        if latitude is None or longitude is None or radius_meters is None:
            return json.dumps({
                "success": False,
                "error": "latitude, longitude, and radius_meters are required"
            })
        
        # Validate latitude (-90 to 90)
        lat_valid = -90 <= latitude <= 90
        
        # Validate longitude (-180 to 180)
        lon_valid = -180 <= longitude <= 180
        
        # Validate radius (10 to 10000 meters)
        radius_valid = 10 <= radius_meters <= 10000
        
        all_valid = lat_valid and lon_valid and radius_valid
        
        return json.dumps({
            "success": True,
            "verified": all_valid,
            "geofence_parameters_valid": all_valid,
            "latitude_valid": lat_valid,
            "longitude_valid": lon_valid,
            "radius_valid": radius_valid
        })
    
    @staticmethod
    def _verify_critical_routines_scheduled(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify if critical routines are scheduled within time window"""
        from datetime import datetime, timedelta

        time_window_hours = verification_data.get("time_window_hours", 2)

        routines = data.get("routines", {})
        current_time_str = verification_data.get("current_time", "2025-10-09T12:00:00Z")

        # Parse current time
        try:
            # Handle both ISO format with and without 'Z'
            if current_time_str.endswith('Z'):
                current_time = datetime.fromisoformat(current_time_str[:-1])
            else:
                current_time = datetime.fromisoformat(current_time_str.replace('T', ' ').split('.')[0])
        except:
            current_time = datetime(2025, 10, 9, 12, 0, 0)

        # Calculate time window
        window_end = current_time + timedelta(hours=time_window_hours)

        critical_scheduled = False
        next_critical_routine = None
        next_execution_time = None
        routines_in_window = []

        for routine_id, routine in routines.items():
            routine_type = routine.get("routine_type", "")
            if "security" in routine_type.lower() or "critical" in routine_type.lower():
                next_execution_str = routine.get("next_execution_time")
                if next_execution_str:
                    try:
                        # Parse next execution time
                        if next_execution_str.endswith('Z'):
                            next_execution = datetime.fromisoformat(next_execution_str[:-1])
                        else:
                            next_execution = datetime.fromisoformat(next_execution_str.replace('T', ' ').split('.')[0])

                        # Check if routine is scheduled within the time window
                        if current_time <= next_execution <= window_end:
                            critical_scheduled = True
                            routines_in_window.append({
                                "routine_id": routine_id,
                                "routine_type": routine_type,
                                "next_execution": next_execution_str
                            })
                            if not next_critical_routine or next_execution < datetime.fromisoformat(next_execution_time.replace('Z', '').replace('T', ' ').split('.')[0]):
                                next_critical_routine = routine_id
                                next_execution_time = next_execution_str
                    except:
                        # Skip routines with invalid timestamp format
                        pass

        return json.dumps({
            "success": True,
            "verified": not critical_scheduled,
            "critical_routines_scheduled": critical_scheduled,
            "next_critical_routine": next_critical_routine,
            "next_execution_time": next_execution_time,
            "routines_in_window": routines_in_window,
            "time_window_hours": time_window_hours,
            "safe_to_update": not critical_scheduled
        })
    
    @staticmethod
    def _verify_energy_monitoring_support(data: Dict[str, Any], device_id: Optional[str]) -> str:
        """Verify device supports energy monitoring"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        capabilities = device.get("capabilities", [])
        energy_monitoring_supported = "energy_monitoring" in capabilities
        
        return json.dumps({
            "success": True,
            "verified": energy_monitoring_supported,
            "device_id": device_id,
            "energy_monitoring_supported": energy_monitoring_supported
        })
    
    @staticmethod
    def _verify_device_capability(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify device has specific capability"""
        device_id = verification_data.get("device_id")
        capability = verification_data.get("capability")
        
        if not device_id or not capability:
            return json.dumps({
                "success": False,
                "error": "device_id and capability are required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        capabilities = device.get("capabilities", [])
        has_capability = capability in capabilities
        
        return json.dumps({
            "success": True,
            "verified": has_capability,
            "device_id": device_id,
            "capability": capability,
            "has_capability": has_capability,
            "available_capabilities": capabilities
        })
    
    @staticmethod
    def _verify_voice_profile_quality(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify voice profile quality meets threshold"""
        user_id = verification_data.get("user_id")
        min_quality_threshold = verification_data.get("min_quality_threshold", 80)
        
        if not user_id:
            return json.dumps({
                "success": False,
                "error": "user_id is required"
            })
        
        voice_profiles = data.get("voice_profiles", {})
        profile = voice_profiles.get(user_id, {})
        quality_score = profile.get("quality_score", 0)
        
        meets_threshold = quality_score >= min_quality_threshold
        
        return json.dumps({
            "success": True,
            "verified": meets_threshold,
            "user_id": user_id,
            "quality_score": quality_score,
            "min_quality_threshold": min_quality_threshold,
            "meets_threshold": meets_threshold
        })
    
    @staticmethod
    def _verify_voice_profile_status(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify voice profile status"""
        user_id = verification_data.get("user_id")
        expected_status = verification_data.get("expected_status", "active")
        
        if not user_id:
            return json.dumps({
                "success": False,
                "error": "user_id is required"
            })
        
        voice_profiles = data.get("voice_profiles", {})
        profile = voice_profiles.get(user_id, {})
        current_status = profile.get("status", "unknown")
        
        status_match = current_status == expected_status
        
        return json.dumps({
            "success": True,
            "verified": status_match,
            "user_id": user_id,
            "current_status": current_status,
            "expected_status": expected_status,
            "status_match": status_match
        })
    
    @staticmethod
    def _verify_routine_trigger_valid(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify routine trigger configuration is valid"""
        trigger_type = verification_data.get("trigger_type")
        trigger_value = verification_data.get("trigger_value")
        
        if not trigger_type:
            return json.dumps({
                "success": False,
                "error": "trigger_type is required"
            })
        
        valid_trigger_types = ["time", "sunrise", "sunset", "location", "sensor", "manual", "voice"]
        
        if trigger_type not in valid_trigger_types:
            return json.dumps({
                "success": True,
                "verified": False,
                "trigger_type": trigger_type,
                "valid": False,
                "error": f"Invalid trigger_type. Must be one of: {', '.join(valid_trigger_types)}"
            })
        
        # Additional validation based on trigger type
        trigger_valid = True
        validation_message = None
        
        if trigger_type == "time" and trigger_value:
            # Validate HH:MM format
            import re
            time_pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
            trigger_valid = bool(re.match(time_pattern, str(trigger_value)))
            if not trigger_valid:
                validation_message = "Time must be in HH:MM format"
        
        elif trigger_type == "location" and trigger_value:
            # Validate location has required fields
            if isinstance(trigger_value, dict):
                required_fields = ["latitude", "longitude", "radius_meters"]
                trigger_valid = all(field in trigger_value for field in required_fields)
                if not trigger_valid:
                    validation_message = f"Location trigger must include: {', '.join(required_fields)}"
            else:
                trigger_valid = False
                validation_message = "Location trigger_value must be a JSON object"
        
        return json.dumps({
            "success": True,
            "verified": trigger_valid,
            "trigger_type": trigger_type,
            "trigger_value": trigger_value,
            "valid": trigger_valid,
            "validation_message": validation_message
        })
    
    @staticmethod
    def _verify_device_type_benchmarks(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify device meets type-specific benchmarks"""
        device_id = verification_data.get("device_id")
        
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        devices = data.get("devices", {})
        device = devices.get(device_id)
        
        if not device:
            return json.dumps({
                "success": False,
                "error": f"Device {device_id} not found"
            })
        
        device_type = device.get("device_type")
        signal_strength = device.get("signal_strength")
        battery_level = device.get("battery_level")
        response_time_ms = device.get("response_time_ms", 0)
        
        # Type-specific benchmarks
        benchmarks = {
            "lock": {"min_signal": -70, "min_battery": 20, "max_response_ms": 2000},
            "camera": {"min_signal": -65, "min_battery": None, "max_response_ms": 1000},
            "thermostat": {"min_signal": -70, "min_battery": None, "max_response_ms": 3000},
            "sensor": {"min_signal": -75, "min_battery": 15, "max_response_ms": 500},
            "light": {"min_signal": -75, "min_battery": None, "max_response_ms": 500}
        }
        
        benchmark = benchmarks.get(device_type, {"min_signal": -70, "min_battery": 20, "max_response_ms": 2000})
        
        meets_benchmarks = True
        failed_criteria = []
        
        if signal_strength is not None and signal_strength < benchmark["min_signal"]:
            meets_benchmarks = False
            failed_criteria.append(f"signal_strength ({signal_strength} dBm < {benchmark['min_signal']} dBm)")
        
        if benchmark["min_battery"] is not None and battery_level is not None:
            if battery_level < benchmark["min_battery"]:
                meets_benchmarks = False
                failed_criteria.append(f"battery_level ({battery_level}% < {benchmark['min_battery']}%)")
        
        if response_time_ms > benchmark["max_response_ms"]:
            meets_benchmarks = False
            failed_criteria.append(f"response_time ({response_time_ms}ms > {benchmark['max_response_ms']}ms)")
        
        return json.dumps({
            "success": True,
            "verified": meets_benchmarks,
            "device_id": device_id,
            "device_type": device_type,
            "meets_benchmarks": meets_benchmarks,
            "benchmarks": benchmark,
            "current_values": {
                "signal_strength": signal_strength,
                "battery_level": battery_level,
                "response_time_ms": response_time_ms
            },
            "failed_criteria": failed_criteria if failed_criteria else None
        })
    
    @staticmethod
    def _verify_network_bandwidth(data: Dict[str, Any], verification_data: Dict[str, Any]) -> str:
        """Verify network bandwidth meets requirements"""
        required_bandwidth_mbps = verification_data.get("required_bandwidth_mbps")
        network_name = verification_data.get("network_name")
        
        if required_bandwidth_mbps is None:
            return json.dumps({
                "success": False,
                "error": "required_bandwidth_mbps is required"
            })
        
        network_status = data.get("network_status", {})
        
        if network_name:
            network = network_status.get(network_name, {})
            available_bandwidth_mbps = network.get("available_bandwidth_mbps", 0)
        else:
            # Check default/primary network
            available_bandwidth_mbps = network_status.get("default_bandwidth_mbps", 0)
        
        sufficient_bandwidth = available_bandwidth_mbps >= required_bandwidth_mbps
        
        return json.dumps({
            "success": True,
            "verified": sufficient_bandwidth,
            "network_name": network_name,
            "required_bandwidth_mbps": required_bandwidth_mbps,
            "available_bandwidth_mbps": available_bandwidth_mbps,
            "sufficient_bandwidth": sufficient_bandwidth
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "confirm_system_state",
                "description": "Verify system states, prerequisites, and requirements. Verification types: 'device_action' (verify device supports action; requires device_id, action), 'device_echo' (verify if device is Echo; requires device_id), 'device_privacy_capabilities' (verify privacy controls support; requires device_id, requested_settings), 'device_network_compatibility' (verify network compatibility; requires device_id, network_frequency), 'skill_compatibility' (verify skill compatibility; requires skill_id), 'update_prerequisites' (verify firmware update readiness; requires device_id), 'pin_configured' (verify PIN configured), 'storage_accessible' (verify storage accessible; requires storage_type), 'storage_space' (verify storage space; requires required_space_mb), 'backup_file_exists' (verify backup exists; requires backup_id), 'backup_checksum' (verify backup integrity; requires backup_id, expected_checksum), 'firmware_version' (verify firmware version; requires device_id, expected_version), 'interior_sensors_disarmed' (verify interior sensors disarmed; requires routine_id), 'announcement_playback' (verify announcement played; requires routine_id), 'security_actions_present' (verify security actions present; requires security_actions), 'perimeter_actions_present' (verify perimeter actions present; requires security_actions), 'no_interior_sensors_armed' (verify no interior sensors armed; requires security_actions), 'armed_stay_requirements' (verify Armed Stay requirements; requires security_actions), 'disarm_requirements' (verify Disarm requirements; requires disarm_actions, voice_trigger), 'disarm_actions_present' (verify disarm actions present; requires disarm_actions), 'routine_has_awareness_actions' (verify routine has awareness actions; requires routine_id), 'geofence_parameters' (verify geofence parameters valid; requires latitude, longitude, radius_meters), 'critical_routines_scheduled' (verify critical routines scheduled; requires time_window_hours), 'energy_monitoring_support' (verify energy monitoring support; requires device_id), 'device_capability' (verify device capability; requires device_id, capability), 'voice_profile_quality' (verify voice profile quality; requires user_id, min_quality_threshold), 'voice_profile_status' (verify voice profile status; requires user_id, expected_status), 'routine_trigger_valid' (verify routine trigger valid; requires trigger_type, trigger_value), 'device_type_benchmarks' (verify device meets benchmarks; requires device_id), 'network_bandwidth' (verify network bandwidth; requires required_bandwidth_mbps, network_name).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "verification_type": {
                            "type": "string",
                            "enum": [
                                "device_action", "device_echo", "device_privacy_capabilities",
                                "device_network_compatibility", "skill_compatibility", "update_prerequisites",
                                "pin_configured", "storage_accessible", "storage_space", "backup_file_exists",
                                "backup_checksum", "firmware_version", "interior_sensors_disarmed",
                                "announcement_playback", "security_actions_present", "perimeter_actions_present",
                                "no_interior_sensors_armed", "armed_stay_requirements", "disarm_requirements",
                                "disarm_actions_present", "routine_has_awareness_actions", "geofence_parameters",
                                "critical_routines_scheduled", "energy_monitoring_support", "device_capability",
                                "voice_profile_quality", "voice_profile_status", "routine_trigger_valid",
                                "device_type_benchmarks", "network_bandwidth"
                            ],
                            "description": "Type of verification to perform"
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Optional entity ID if verification relates to specific entity (e.g., device_id for device-specific verifications)"
                        },
                        "verification_data": {
                            "type": "object",
                            "description": "JSON object with verification-specific parameters. SYNTAX: {\"key\": \"value\"} for single parameter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple parameters. REQUIRED FIELDS BY TYPE: device_action (device_id, action), device_echo (device_id), device_privacy_capabilities (device_id, requested_settings), device_network_compatibility (device_id, network_frequency), skill_compatibility (skill_id), update_prerequisites (device_id), storage_accessible (storage_type: 'cloud' or 'local'), storage_space (required_space_mb), backup_file_exists (backup_id), backup_checksum (backup_id, expected_checksum), firmware_version (device_id, expected_version), interior_sensors_disarmed (routine_id), announcement_playback (routine_id), security_actions_present (security_actions: array), perimeter_actions_present (security_actions: array), no_interior_sensors_armed (security_actions: array), armed_stay_requirements (security_actions: array), disarm_requirements (disarm_actions: array, voice_trigger: boolean), disarm_actions_present (disarm_actions: array), routine_has_awareness_actions (routine_id), geofence_parameters (latitude, longitude, radius_meters), critical_routines_scheduled (time_window_hours), energy_monitoring_support (device_id), device_capability (device_id, capability), voice_profile_quality (user_id, min_quality_threshold), voice_profile_status (user_id, expected_status), routine_trigger_valid (trigger_type, trigger_value), device_type_benchmarks (device_id), network_bandwidth (required_bandwidth_mbps, network_name: optional)"
                        }
                    },
                    "required": ["verification_type", "verification_data"]
                }
            }
        }