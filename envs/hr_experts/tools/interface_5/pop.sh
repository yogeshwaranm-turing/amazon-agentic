#!/bin/bash

# Create HR Discovery Tools Python Files
# This script creates individual Python files for each HR discovery tool

# Create directory if it doesn't exist
mkdir -p hr_tools

# Create discover_payroll_entities.py
cat > hr_tools/discover_payroll_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPayrollEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover payroll entities.
        
        Supported entities:
        - payroll_records: Payroll records by payroll_id, employee_id, pay_period_start, pay_period_end, hours_worked, hourly_rate, payment_date, status, approved_by, created_at, updated_at
        - payroll_deductions: Payroll deductions by deduction_id, payroll_id, deduction_type, amount, created_by, created_at
        """
        if entity_type not in ["payroll_records", "payroll_deductions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'payroll_records' or 'payroll_deductions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "payroll_id" if entity_type == "payroll_records" else "deduction_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_payroll_entities",
                "description": "Discover payroll entities. Entity types: 'payroll_records' (payroll records; filterable by payroll_id (string), employee_id (string), pay_period_start (date), pay_period_end (date), hours_worked (decimal), hourly_rate (decimal), payment_date (date), status (enum: 'draft', 'approved', 'paid', 'cancelled'), approved_by (string), created_at (timestamp), updated_at (timestamp)), 'payroll_deductions' (payroll deductions; filterable by deduction_id (string), payroll_id (string), deduction_type (enum: 'tax', 'insurance', 'retirement', 'garnishment', 'equipment', 'other'), amount (decimal), created_by (string), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'payroll_records' or 'payroll_deductions'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For payroll_records, filters are: payroll_id (string), employee_id (string), pay_period_start (date), pay_period_end (date), hours_worked (decimal), hourly_rate (decimal), payment_date (date), status (enum: 'draft', 'approved', 'paid', 'cancelled'), approved_by (string), created_at (timestamp), updated_at (timestamp). For payroll_deductions, filters are: deduction_id (string), payroll_id (string), deduction_type (enum: 'tax', 'insurance', 'retirement', 'garnishment', 'equipment', 'other'), amount (decimal), created_by (string), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_benefits_entities.py
cat > hr_tools/discover_benefits_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverBenefitsEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover benefits entities.
        
        Supported entities:
        - benefits_plans: Benefits plans by plan_id, plan_name, plan_type, provider, employee_cost, employer_cost, status, effective_date, expiration_date, created_at, updated_at
        - employee_benefits: Employee benefits by enrollment_id, employee_id, plan_id, enrollment_date, status, coverage_level, beneficiary_name, beneficiary_relationship, created_at, updated_at
        """
        if entity_type not in ["benefits_plans", "employee_benefits"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'benefits_plans' or 'employee_benefits'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "plan_id" if entity_type == "benefits_plans" else "enrollment_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_benefits_entities",
                "description": "Discover benefits entities. Entity types: 'benefits_plans' (benefits plans; filterable by plan_id (string), plan_name (string), plan_type (enum: 'health_insurance', 'dental', 'vision', 'life_insurance', 'disability', 'retirement_401k', 'pto', 'flexible_spending'), provider (string), employee_cost (decimal), employer_cost (decimal), status (enum: 'active', 'inactive'), effective_date (date), expiration_date (date), created_at (timestamp), updated_at (timestamp)), 'employee_benefits' (employee benefits; filterable by enrollment_id (string), employee_id (string), plan_id (string), enrollment_date (date), status (enum: 'active', 'terminated', 'pending'), coverage_level (enum: 'employee_only', 'employee_spouse', 'employee_children', 'family'), beneficiary_name (string), beneficiary_relationship (string), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'benefits_plans' or 'employee_benefits'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For benefits_plans, filters are: plan_id (string), plan_name (string), plan_type (enum: 'health_insurance', 'dental', 'vision', 'life_insurance', 'disability', 'retirement_401k', 'pto', 'flexible_spending'), provider (string), employee_cost (decimal), employer_cost (decimal), status (enum: 'active', 'inactive'), effective_date (date), expiration_date (date), created_at (timestamp), updated_at (timestamp). For employee_benefits, filters are: enrollment_id (string), employee_id (string), plan_id (string), enrollment_date (date), status (enum: 'active', 'terminated', 'pending'), coverage_level (enum: 'employee_only', 'employee_spouse', 'employee_children', 'family'), beneficiary_name (string), beneficiary_relationship (string), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_performance_entities.py
cat > hr_tools/discover_performance_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPerformanceEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover performance entities.
        
        Supported entities:
        - performance_reviews: Performance reviews by review_id, employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating, goals_achievement_score, communication_score, teamwork_score, leadership_score, technical_skills_score, status, created_at, updated_at
        """
        if entity_type not in ["performance_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'performance_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("performance_reviews", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "review_id": entity_id})
            else:
                results.append({**entity_data, "review_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_performance_entities",
                "description": "Discover performance entities. Entity types: 'performance_reviews' (performance reviews; filterable by review_id (string), employee_id (string), reviewer_id (string), review_period_start (date), review_period_end (date), review_type (enum: 'annual', 'quarterly', 'probationary', 'project_based'), overall_rating (enum: 'exceeds_expectations', 'meets_expectations', 'below_expectations', 'unsatisfactory'), goals_achievement_score (decimal), communication_score (decimal), teamwork_score (decimal), leadership_score (decimal), technical_skills_score (decimal), status (enum: 'draft', 'submitted', 'approved'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'performance_reviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For performance_reviews, filters are: review_id (string), employee_id (string), reviewer_id (string), review_period_start (date), review_period_end (date), review_type (enum: 'annual', 'quarterly', 'probationary', 'project_based'), overall_rating (enum: 'exceeds_expectations', 'meets_expectations', 'below_expectations', 'unsatisfactory'), goals_achievement_score (decimal), communication_score (decimal), teamwork_score (decimal), leadership_score (decimal), technical_skills_score (decimal), status (enum: 'draft', 'submitted', 'approved'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_leave_entities.py
cat > hr_tools/discover_leave_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverLeaveEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover leave entities.
        
        Supported entities:
        - leave_requests: Leave requests by leave_id, employee_id, leave_type, start_date, end_date, days_requested, status, approved_by, approval_date, remaining_balance, created_at, updated_at
        """
        if entity_type not in ["leave_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'leave_requests'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("leave_requests", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "leave_id": entity_id})
            else:
                results.append({**entity_data, "leave_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_leave_entities",
                "description": "Discover leave entities. Entity types: 'leave_requests' (leave requests; filterable by leave_id (string), employee_id (string), leave_type (enum: 'annual', 'sick', 'fmla', 'personal', 'bereavement', 'jury_duty'), start_date (date), end_date (date), days_requested (decimal), status (enum: 'pending', 'approved', 'rejected', 'cancelled'), approved_by (string), approval_date (timestamp), remaining_balance (decimal), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'leave_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For leave_requests, filters are: leave_id (string), employee_id (string), leave_type (enum: 'annual', 'sick', 'fmla', 'personal', 'bereavement', 'jury_duty'), start_date (date), end_date (date), days_requested (decimal), status (enum: 'pending', 'approved', 'rejected', 'cancelled'), approved_by (string), approval_date (timestamp), remaining_balance (decimal), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_expense_entities.py
cat > hr_tools/discover_expense_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverExpenseEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover expense entities.
        
        Supported entities:
        - expense_reimbursements: Expense reimbursements by reimbursement_id, employee_id, expense_date, amount, expense_type, receipt_file_path, status, approved_by, payment_date, created_at, updated_at
        """
        if entity_type not in ["expense_reimbursements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'expense_reimbursements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("expense_reimbursements", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "reimbursement_id": entity_id})
            else:
                results.append({**entity_data, "reimbursement_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_expense_entities",
                "description": "Discover expense entities. Entity types: 'expense_reimbursements' (expense reimbursements; filterable by reimbursement_id (string), employee_id (string), expense_date (date), amount (decimal), expense_type (enum: 'travel', 'meals', 'equipment', 'training', 'other'), receipt_file_path (string), status (enum: 'submitted', 'approved', 'rejected', 'paid'), approved_by (string), payment_date (date), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'expense_reimbursements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For expense_reimbursements, filters are: reimbursement_id (string), employee_id (string), expense_date (date), amount (decimal), expense_type (enum: 'travel', 'meals', 'equipment', 'training', 'other'), receipt_file_path (string), status (enum: 'submitted', 'approved', 'rejected', 'paid'), approved_by (string), payment_date (date), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_training_entities.py
cat > hr_tools/discover_training_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverTrainingEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover training entities.
        
        Supported entities:
        - training_programs: Training programs by program_id, program_name, program_type, duration_hours, delivery_method, mandatory, status, created_at, updated_at
        - employee_training: Employee training records by training_record_id, employee_id, program_id, enrollment_date, completion_date, status, score, certificate_issued, expiry_date, created_at, updated_at
        """
        if entity_type not in ["training_programs", "employee_training"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'training_programs' or 'employee_training'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "program_id" if entity_type == "training_programs" else "training_record_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_training_entities",
                "description": "Discover training entities. Entity types: 'training_programs' (training programs; filterable by program_id (string), program_name (string), program_type (enum: 'onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics'), duration_hours (integer), delivery_method (enum: 'in_person', 'online', 'hybrid', 'self_paced'), mandatory (boolean), status (enum: 'active', 'inactive', 'draft'), created_at (timestamp), updated_at (timestamp)), 'employee_training' (employee training records; filterable by training_record_id (string), employee_id (string), program_id (string), enrollment_date (date), completion_date (date), status (enum: 'enrolled', 'in_progress', 'completed', 'failed', 'cancelled'), score (decimal), certificate_issued (boolean), expiry_date (date), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'training_programs' or 'employee_training'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For training_programs, filters are: program_id (string), program_name (string), program_type (enum: 'onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics'), duration_hours (integer), delivery_method (enum: 'in_person', 'online', 'hybrid', 'self_paced'), mandatory (boolean), status (enum: 'active', 'inactive', 'draft'), created_at (timestamp), updated_at (timestamp). For employee_training, filters are: training_record_id (string), employee_id (string), program_id (string), enrollment_date (date), completion_date (date), status (enum: 'enrolled', 'in_progress', 'completed', 'failed', 'cancelled'), score (decimal), certificate_issued (boolean), expiry_date (date), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

# Create discover_document_entities.py
cat > hr_tools/discover_document_entities.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverDocumentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover document entities.
        
        Supported entities:
        - document_storage: Document storage records by document_id, document_name, document_type, employee_id, file_path, upload_date, uploaded_by, confidentiality_level, retention_period_years, expiry_date, status, created_at
        """
        if entity_type not in ["document_storage"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'document_storage'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("document_storage", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "document_id": entity_id})
            else:
                results.append({**entity_data, "document_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_document_entities",
                "description": "Discover document entities. Entity types: 'document_storage' (document storage records; filterable by document_id (string), document_name (string), document_type (enum: 'contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter'), employee_id (string), file_path (string), upload_date (timestamp), uploaded_by (string), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), retention_period_years (integer), expiry_date (date), status (enum: 'active', 'archived', 'deleted'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'document_storage'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For document_storage, filters are: document_id (string), document_name (string), document_type (enum: 'contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter'), employee_id (string), file_path (string), upload_date (timestamp), uploaded_by (string), confidentiality_level (enum: 'public', 'internal', 'confidential', 'restricted'), retention_period_years (integer), expiry_date (date), status (enum: 'active', 'archived', 'deleted'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF