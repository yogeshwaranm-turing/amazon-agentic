#!/usr/bin/env python3
"""
WIKI SEED DATA GENERATOR

This script generates realistic test data for a wiki system following the provided schema.
It generates data with proper relationships, realistic content, and consistent results.

USAGE:
    python3 create_wiki_seeds.py

OUTPUT:
    - Deletes all existing JSON files in ./data/
    - Generates fresh data with all business rules
    - Creates JSON files with complete dataset

FEATURES:
    ✓ Consistent results with fixed seeds
    ✓ Realistic user roles and space memberships
    ✓ Proper page hierarchies and versioning
    ✓ Comprehensive permission management
    ✓ Audit logging and notifications
    ✓ Export jobs and approval workflows
"""

import json
import random
import datetime as dt_module
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path
import glob
import os

# Fixed seeds for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Fixed reference date for reproducibility
REFERENCE_DATE = datetime(2025, 10, 20, 20, 50, 37)
MAX_DATE = REFERENCE_DATE

# Configuration
EMAIL_DOMAINS = ['siemens.com', 'gmail.com', 'outlook.com', 'company.com', 'techcorp.com']

# User role distribution (realistic for a wiki system)
USER_ROLE_DISTRIBUTION = {
    'global_admin': 5,
    'space_admin': 25,
    'space_member': 150,
    'content_contributor': 80,
    'reviewer_approver': 30,
    'guest': 20,
    'project_team_admin': 15,
    'anonymous': 10
}

# Space feature configurations
SPACE_FEATURES = ['live_docs', 'calendars', 'whiteboard', 'databases', 'smart_links', 'folders', 'blogs']

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_email(first_name, last_name, used_emails):
    """Generate unique realistic email addresses"""
    domain = random.choice(EMAIL_DOMAINS)
    counter = 1
    while True:
        if counter == 1:
            email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        else:
            email = f"{first_name.lower()}.{last_name.lower()}{counter}@{domain}"
        
        if email not in used_emails:
            used_emails.add(email)
            return email
        counter += 1

def format_timestamp(dt_obj):
    """Format a datetime object to YYYY-MM-DDTHH:MM:SS"""
    if dt_obj is None:
        return None
    if isinstance(dt_obj, dt_module.datetime):
        return dt_obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(dt_obj, dt_module.date):
        return dt_obj.strftime('%Y-%m-%d')
    return str(dt_obj)

def generate_timestamp(start_date=None, end_date=None):
    """Generate random timestamp within range"""
    if start_date is None:
        start_date = MAX_DATE - timedelta(days=365)
    if end_date is None:
        end_date = MAX_DATE
    
    if end_date > MAX_DATE:
        end_date = MAX_DATE
    
    if isinstance(start_date, dt_module.date) and not isinstance(start_date, dt_module.datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    
    time_between = end_date - start_date
    total_seconds = int(time_between.total_seconds())
    
    if total_seconds <= 0:
        return start_date
    
    random_seconds_offset = random.randrange(total_seconds)
    result = start_date + timedelta(seconds=random_seconds_offset)
    
    if result > MAX_DATE:
        result = MAX_DATE
    
    return result

def generate_timestamps(max_age_days=90):
    """Generate created_at and updated_at with proper ordering"""
    start = MAX_DATE - timedelta(days=max_age_days)
    end_for_created = MAX_DATE - timedelta(hours=1)
    
    created_dt = generate_timestamp(start, end_for_created)
    updated_dt = generate_timestamp(created_dt, MAX_DATE)
    
    return format_timestamp(created_dt), format_timestamp(updated_dt)

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_users():
    """Generate users with role-based distribution"""
    users = {}
    user_id = 1
    used_emails = set()
    
    for role, count in USER_ROLE_DISTRIBUTION.items():
        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            created, _ = generate_timestamps(max_age_days=random.randint(30, 365))
            
            users[str(user_id)] = {
                "user_id": str(user_id),
                "email": generate_email(first_name, last_name, used_emails),
                "account_id": f"ACC{str(user_id).zfill(6)}",
                "full_name": f"{first_name} {last_name}",
                "global_role": role,
                "created_at": created
            }
            user_id += 1
    
    return users

def generate_groups():
    """Generate user groups"""
    groups = {}
    group_names = [
        "Engineering Team", "Product Management", "Design Team", "QA Team",
        "DevOps Team", "Marketing Team", "Sales Team", "Support Team",
        "Documentation Team", "Research Team", "Security Team", "Analytics Team",
        "Project Alpha", "Project Beta", "Project Gamma", "Mobile Team",
        "Frontend Team", "Backend Team", "Data Science Team", "Infrastructure Team"
    ]
    
    for i, group_name in enumerate(group_names, 1):
        created, _ = generate_timestamps(max_age_days=random.randint(60, 300))
        
        groups[str(i)] = {
            "group_id": str(i),
            "group_name": group_name,
            "created_at": created
        }
    
    return groups

def generate_user_groups(users, groups):
    """Generate user-group memberships"""
    user_groups = {}
    membership_id = 1
    
    for user_id in users.keys():
        # Each user belongs to 1-3 groups
        num_groups = random.randint(1, 3)
        selected_groups = random.sample(list(groups.keys()), min(num_groups, len(groups)))
        
        for group_id in selected_groups:
            joined_at, _ = generate_timestamps(max_age_days=random.randint(1, 180))
            
            user_groups[str(membership_id)] = {
                "user_id": user_id,
                "group_id": group_id,
                "joined_at": joined_at
            }
            membership_id += 1
    
    return user_groups

def generate_spaces(users):
    """Generate wiki spaces"""
    spaces = {}
    space_purposes = [
        "Product documentation and specifications",
        "Engineering knowledge base and best practices",
        "Project planning and collaboration space",
        "Team meeting notes and decisions",
        "API documentation and developer guides",
        "Customer support knowledge base",
        "Design system and UI guidelines",
        "Security policies and procedures",
        "Marketing campaigns and strategies",
        "Sales playbooks and training materials",
        "HR policies and employee handbook",
        "Quality assurance testing procedures",
        "DevOps runbooks and infrastructure docs",
        "Research findings and analysis",
        "Training materials and tutorials"
    ]
    
    space_keys = [
        "PROD", "ENG", "PROJ", "TEAM", "API", "SUPP", "DESIGN", "SEC",
        "MARK", "SALES", "HR", "QA", "DEVOPS", "RES", "TRAIN", "DOCS",
        "ARCH", "DATA", "MOB", "WEB", "INFRA", "COMP", "LEGAL", "FIN",
        "OPS", "STRAT", "INNOV", "PART", "COMM", "EVENTS"
    ]
    
    for i in range(1, 31):  # 30 spaces
        created, _ = generate_timestamps(max_age_days=random.randint(30, 365))
        
        spaces[str(i)] = {
            "space_id": str(i),
            "space_key": space_keys[i-1],
            "space_name": f"{space_keys[i-1]} - {fake.catch_phrase()}",
            "space_purpose": random.choice(space_purposes),
            "created_by_user_id": random.choice(list(users.keys())),
            "created_at": created,
            "is_deleted": random.choice([False] * 95 + [True] * 5),  # 5% deleted
            "deleted_at": format_timestamp(generate_timestamp(
                datetime.fromisoformat(created), MAX_DATE
            )) if random.random() < 0.05 else None
        }
    
    return spaces

def generate_space_memberships(users, spaces):
    """Generate space memberships"""
    memberships = {}
    membership_id = 1
    
    for space_id, space in spaces.items():
        if space['is_deleted']:
            continue
            
        # Each space has 3-15 members
        num_members = random.randint(3, 15)
        selected_users = random.sample(list(users.keys()), min(num_members, len(users)))
        
        # Ensure space creator is a member with admin role
        if space['created_by_user_id'] not in selected_users:
            selected_users[0] = space['created_by_user_id']
        
        for i, user_id in enumerate(selected_users):
            if user_id == space['created_by_user_id']:
                role = 'space_admin'
            else:
                role = random.choice(['space_member'] * 7 + ['space_admin'] * 2 + ['content_contributor'] * 1)
            
            joined_at, _ = generate_timestamps(max_age_days=random.randint(1, 200))
            
            memberships[str(membership_id)] = {
                "user_id": user_id,
                "space_id": space_id,
                "role": role,
                "joined_at": joined_at
            }
            membership_id += 1
    
    return memberships

def generate_space_features(spaces):
    """Generate space features"""
    features = {}
    feature_id = 1
    
    for space_id, space in spaces.items():
        if space['is_deleted']:
            continue
            
        # Each space has 3-6 features enabled
        num_features = random.randint(3, 6)
        selected_features = random.sample(SPACE_FEATURES, num_features)
        
        for feature_type in selected_features:
            features[str(feature_id)] = {
                "feature_id": str(feature_id),
                "space_id": space_id,
                "feature_type": feature_type,
                "is_enabled": random.choice([True] * 9 + [False] * 1)  # 90% enabled
            }
            feature_id += 1
    
    return features

def generate_pages(spaces, users):
    """Generate wiki pages with hierarchical structure"""
    pages = {}
    page_id = 1
    
    page_titles = [
        "Getting Started Guide", "API Documentation", "Best Practices", "Troubleshooting",
        "Architecture Overview", "Installation Guide", "Configuration", "User Manual",
        "FAQ", "Release Notes", "Security Guidelines", "Performance Tuning",
        "Integration Guide", "Development Setup", "Testing Procedures", "Deployment Guide",
        "Monitoring and Alerts", "Backup and Recovery", "Data Migration", "Team Processes",
        "Code Review Guidelines", "Git Workflow", "CI/CD Pipeline", "Docker Setup",
        "Database Schema", "API Reference", "SDK Documentation", "Mobile App Guide",
        "Web Interface", "Admin Panel", "User Permissions", "Audit Logs",
        "Compliance Requirements", "Privacy Policy", "Terms of Service", "Support Contacts"
    ]
    
    for space_id, space in spaces.items():
        if space['is_deleted']:
            continue
            
        # Each space has 5-20 pages
        num_pages = random.randint(5, 20)
        
        for i in range(num_pages):
            created, updated = generate_timestamps(max_age_days=random.randint(1, 180))
            
            # 20% chance of having a parent page (for hierarchy)
            parent_page_id = None
            if i > 0 and random.random() < 0.2:
                # Select from existing pages in this space
                space_pages = [p_id for p_id, p in pages.items() if p['space_id'] == space_id]
                if space_pages:
                    parent_page_id = random.choice(space_pages)
            
            state = random.choice(['draft'] * 2 + ['published'] * 7 + ['archived'] * 1)
            is_published = state == 'published'
            
            pages[str(page_id)] = {
                "page_id": str(page_id),
                "space_id": space_id,
                "parent_page_id": parent_page_id,
                "title": random.choice(page_titles),
                "content_format": random.choice(['markdown'] * 6 + ['html'] * 3 + ['richtext'] * 1),
                "current_version": random.randint(1, 10),
                "state": state,
                "created_by_user_id": random.choice(list(users.keys())),
                "updated_by_user_id": random.choice(list(users.keys())),
                "created_at": created,
                "updated_at": updated,
                "is_trashed": random.choice([False] * 95 + [True] * 5),
                "is_published": is_published
            }
            page_id += 1
    
    return pages

def generate_page_versions(pages, users):
    """Generate page version history"""
    versions = {}
    version_id = 1
    
    for page_id, page in pages.items():
        current_version = page['current_version']
        page_created = datetime.fromisoformat(page['created_at'])
        page_updated = datetime.fromisoformat(page['updated_at'])
        
        # Generate versions from 1 to current_version
        for version_num in range(1, current_version + 1):
            if version_num == 1:
                edited_at = page_created
            else:
                # Distribute versions between created and updated
                version_progress = (version_num - 1) / (current_version - 1) if current_version > 1 else 0
                time_diff = page_updated - page_created
                edited_at = page_created + timedelta(seconds=time_diff.total_seconds() * version_progress)
            
            content_snapshot = f"Version {version_num} content for page: {page['title']}\n\n"
            content_snapshot += fake.text(max_nb_chars=500)
            
            versions[str(version_id)] = {
                "version_id": str(version_id),
                "page_id": page_id,
                "version_number": version_num,
                "editor_user_id": random.choice(list(users.keys())),
                "edited_at": format_timestamp(edited_at),
                "content_snapshot": content_snapshot
            }
            version_id += 1
    
    return versions

def generate_permissions(spaces, pages, users, groups):
    """Generate permission records"""
    permissions = {}
    permission_id = 1
    
    # Space-level permissions
    for space_id in spaces.keys():
        # 3-8 permission records per space
        num_permissions = random.randint(3, 8)
        
        for _ in range(num_permissions):
            granted_at, _ = generate_timestamps(max_age_days=random.randint(1, 180))
            
            # Either user or group permission (mutually exclusive)
            if random.random() < 0.7:  # 70% user permissions
                user_id = random.choice(list(users.keys()))
                group_id = None
            else:  # 30% group permissions
                user_id = None
                group_id = random.choice(list(groups.keys()))
            
            is_active = random.choice([True] * 9 + [False] * 1)
            revoked_at = None
            revoked_by_user_id = None
            
            if not is_active:
                revoked_at = format_timestamp(generate_timestamp(
                    datetime.fromisoformat(granted_at), MAX_DATE
                ))
                revoked_by_user_id = random.choice(list(users.keys()))
            
            # Expires in 30-365 days (50% chance)
            expires_at = None
            if random.random() < 0.5:
                expires_at = format_timestamp(generate_timestamp(
                    datetime.fromisoformat(granted_at),
                    datetime.fromisoformat(granted_at) + timedelta(days=random.randint(30, 365))
                ))
            
            permissions[str(permission_id)] = {
                "permission_id": str(permission_id),
                "space_id": space_id,
                "page_id": None,
                "user_id": user_id,
                "group_id": group_id,
                "permission_type": random.choice(['view'] * 5 + ['edit'] * 3 + ['admin'] * 2),
                "granted_by_user_id": random.choice(list(users.keys())),
                "granted_at": granted_at,
                "is_active": is_active,
                "revoked_by_user_id": revoked_by_user_id,
                "revoked_at": revoked_at,
                "expires_at": expires_at
            }
            permission_id += 1
    
    # Page-level permissions (fewer, more specific)
    page_list = list(pages.keys())
    selected_pages = random.sample(page_list, min(50, len(page_list)))  # 50 pages with specific permissions
    
    for page_id in selected_pages:
        num_permissions = random.randint(1, 3)
        
        for _ in range(num_permissions):
            granted_at, _ = generate_timestamps(max_age_days=random.randint(1, 120))
            
            if random.random() < 0.8:  # 80% user permissions for pages
                user_id = random.choice(list(users.keys()))
                group_id = None
            else:
                user_id = None
                group_id = random.choice(list(groups.keys()))
            
            is_active = random.choice([True] * 95 + [False] * 5)
            revoked_at = None
            revoked_by_user_id = None
            
            if not is_active:
                revoked_at = format_timestamp(generate_timestamp(
                    datetime.fromisoformat(granted_at), MAX_DATE
                ))
                revoked_by_user_id = random.choice(list(users.keys()))
            
            permissions[str(permission_id)] = {
                "permission_id": str(permission_id),
                "space_id": None,
                "page_id": page_id,
                "user_id": user_id,
                "group_id": group_id,
                "permission_type": random.choice(['view'] * 4 + ['edit'] * 5 + ['admin'] * 1),
                "granted_by_user_id": random.choice(list(users.keys())),
                "granted_at": granted_at,
                "is_active": is_active,
                "revoked_by_user_id": revoked_by_user_id,
                "revoked_at": revoked_at,
                "expires_at": None  # Page permissions typically don't expire
            }
            permission_id += 1
    
    return permissions

def generate_watchers(spaces, pages, users, groups):
    """Generate watchers for spaces and pages"""
    watchers = {}
    watcher_id = 1
    
    # Space watchers
    for space_id in spaces.keys():
        num_watchers = random.randint(2, 8)
        
        for _ in range(num_watchers):
            watched_at, _ = generate_timestamps(max_age_days=random.randint(1, 200))
            
            if random.random() < 0.8:  # 80% user watchers
                user_id = random.choice(list(users.keys()))
                group_id = None
            else:
                user_id = None
                group_id = random.choice(list(groups.keys()))
            
            watchers[str(watcher_id)] = {
                "watcher_id": str(watcher_id),
                "user_id": user_id,
                "group_id": group_id,
                "space_id": space_id,
                "page_id": None,
                "watched_at": watched_at
            }
            watcher_id += 1
    
    # Page watchers (subset of pages)
    page_list = list(pages.keys())
    selected_pages = random.sample(page_list, min(80, len(page_list)))
    
    for page_id in selected_pages:
        num_watchers = random.randint(1, 5)
        
        for _ in range(num_watchers):
            watched_at, _ = generate_timestamps(max_age_days=random.randint(1, 150))
            
            if random.random() < 0.9:  # 90% user watchers for pages
                user_id = random.choice(list(users.keys()))
                group_id = None
            else:
                user_id = None
                group_id = random.choice(list(groups.keys()))
            
            watchers[str(watcher_id)] = {
                "watcher_id": str(watcher_id),
                "user_id": user_id,
                "group_id": group_id,
                "space_id": None,
                "page_id": page_id,
                "watched_at": watched_at
            }
            watcher_id += 1
    
    return watchers

def generate_export_jobs(spaces, users):
    """Generate export jobs"""
    export_jobs = {}
    job_id = 1
    
    # Generate 40 export jobs
    for i in range(1, 41):
        requested_at, _ = generate_timestamps(max_age_days=random.randint(1, 90))
        
        status = random.choice(['pending'] * 1 + ['running'] * 1 + ['completed'] * 6 + ['failed'] * 1 + ['cancelled'] * 1)
        
        export_jobs[str(job_id)] = {
            "job_id": str(job_id),
            "space_id": random.choice(list(spaces.keys())),
            "requested_by_user_id": random.choice(list(users.keys())),
            "requested_at": requested_at,
            "status": status,
            "format": random.choice(['PDF'] * 5 + ['HTML'] * 3 + ['XML'] * 2),
            "destination": f"s3://wiki-exports/job_{job_id}/export.{random.choice(['pdf', 'html', 'xml'])}",
            "estimated_size_kb": random.randint(100, 50000),
            "priority": random.randint(0, 5)
        }
        job_id += 1
    
    return export_jobs

def generate_audit_logs(users, spaces, pages):
    """Generate audit log entries"""
    audit_logs = {}
    log_id = 1
    
    actions = [
        'create_space', 'update_space', 'delete_space', 'manage_permissions',
        'grant_admin_rights', 'configure_settings', 'export_space', 'import_space',
        'create_page', 'update_page', 'delete_page', 'move_page', 'rename_page',
        'restore_version', 'clone_page', 'publish_page', 'unpublish_page',
        'archive_content', 'watch_content', 'unwatch_content'
    ]
    
    # Generate 200 audit log entries
    for i in range(1, 201):
        occurred_at, _ = generate_timestamps(max_age_days=random.randint(1, 180))
        action_type = random.choice(actions)
        
        # Determine target entity based on action
        if 'space' in action_type:
            target_entity_type = 'space'
            target_entity_id = random.choice(list(spaces.keys()))
        elif 'page' in action_type or 'content' in action_type:
            target_entity_type = 'page'
            target_entity_id = random.choice(list(pages.keys()))
        else:
            target_entity_type = random.choice(['space', 'page'])
            if target_entity_type == 'space':
                target_entity_id = random.choice(list(spaces.keys()))
            else:
                target_entity_id = random.choice(list(pages.keys()))
        
        # Generate realistic details
        details = {
            "action": action_type,
            "timestamp": occurred_at,
            "user_agent": fake.user_agent(),
            "ip_address": fake.ipv4(),
            "changes": {
                "field": random.choice(['title', 'content', 'permissions', 'status']),
                "old_value": fake.word(),
                "new_value": fake.word()
            }
        }
        
        audit_logs[str(log_id)] = {
            "log_id": str(log_id),
            "actor_user_id": random.choice(list(users.keys())),
            "action_type": action_type,
            "target_entity_type": target_entity_type,
            "target_entity_id": target_entity_id,
            "occurred_at": occurred_at,
            "details": details
        }
        log_id += 1
    
    return audit_logs

def generate_space_config_history(spaces, users):
    """Generate space configuration history"""
    config_history = {}
    history_id = 1
    
    # Generate 60 configuration changes
    for i in range(1, 61):
        space_id = random.choice(list(spaces.keys()))
        changed_at, _ = generate_timestamps(max_age_days=random.randint(1, 120))
        
        old_config = {
            "theme": random.choice(["default", "dark", "light"]),
            "permissions": {
                "default_view": random.choice([True, False]),
                "allow_anonymous": random.choice([True, False])
            },
            "features": {
                "comments_enabled": random.choice([True, False]),
                "versioning_enabled": random.choice([True, False])
            }
        }
        
        new_config = {
            "theme": random.choice(["default", "dark", "light"]),
            "permissions": {
                "default_view": random.choice([True, False]),
                "allow_anonymous": random.choice([True, False])
            },
            "features": {
                "comments_enabled": random.choice([True, False]),
                "versioning_enabled": random.choice([True, False])
            }
        }
        
        config_history[str(history_id)] = {
            "history_id": str(history_id),
            "space_id": space_id,
            "changed_by_user_id": random.choice(list(users.keys())),
            "changed_at": changed_at,
            "config_version": random.randint(1, 10),
            "old_config": old_config,
            "new_config": new_config
        }
        history_id += 1
    
    return config_history

def generate_approval_requests(pages, users):
    """Generate approval requests"""
    approval_requests = {}
    request_id = 1
    
    # Generate 50 approval requests
    for i in range(1, 51):
        created_at, updated_at = generate_timestamps(max_age_days=random.randint(1, 60))
        
        status = random.choice(['pending'] * 2 + ['in_review'] * 2 + ['approved'] * 4 + ['rejected'] * 1 + ['cancelled'] * 1)
        
        # Due date 3-14 days from creation
        due_at = format_timestamp(
            datetime.fromisoformat(created_at) + timedelta(days=random.randint(3, 14))
        )
        
        approval_requests[str(request_id)] = {
            "request_id": str(request_id),
            "target_entity_type": "page",
            "target_entity_id": random.choice(list(pages.keys())),
            "requested_by_user_id": random.choice(list(users.keys())),
            "status": status,
            "reason": fake.sentence(),
            "created_at": created_at,
            "updated_at": updated_at,
            "due_at": due_at
        }
        request_id += 1
    
    return approval_requests

def generate_approval_decisions(approval_requests, users):
    """Generate approval decisions with step_id as string"""
    decisions = {}
    decision_id = 1
    
    # Generate decisions for approved/rejected requests
    for request_id, request in approval_requests.items():
        if request['status'] in ['approved', 'rejected', 'in_review']:
            # Generate 1-2 decisions per request
            num_decisions = random.randint(1, 2)
            
            for step_num in range(1, num_decisions + 1):
                decided_at, _ = generate_timestamps(max_age_days=random.randint(1, 45))
                
                if request['status'] == 'approved':
                    decision_type = 'approve'
                elif request['status'] == 'rejected':
                    decision_type = 'reject'
                else:  # in_review
                    decision_type = random.choice(['approve', 'escalate'])
                
                decisions[str(decision_id)] = {
                    "decision_id": str(decision_id),
                    "step_id": f"STEP_{request_id}_{step_num}",  # String step identifier
                    "approver_user_id": random.choice(list(users.keys())),
                    "decision": decision_type,
                    "comment": fake.sentence() if random.random() < 0.7 else None,
                    "decided_at": decided_at
                }
                decision_id += 1
    
    return decisions

def generate_notifications(users, spaces, pages):
    """Generate notifications without metadata field"""
    notifications = {}
    notification_id = 1
    
    event_types = [
        'page_created', 'page_updated', 'page_deleted', 'page_commented',
        'space_created', 'space_updated', 'permission_granted', 'permission_revoked',
        'approval_requested', 'approval_approved', 'approval_rejected',
        'export_completed', 'export_failed', 'mention_received'
    ]
    
    # Generate 300 notifications
    for i in range(1, 301):
        created_at, _ = generate_timestamps(max_age_days=random.randint(1, 90))
        
        event_type = random.choice(event_types)
        delivery_status = random.choice(['pending'] * 1 + ['sent'] * 7 + ['delivered'] * 2)
        
        sent_at = None
        read_at = None
        
        if delivery_status in ['sent', 'delivered']:
            sent_at = format_timestamp(
                datetime.fromisoformat(created_at) + timedelta(minutes=random.randint(1, 30))
            )
            
            if delivery_status == 'delivered' and random.random() < 0.6:  # 60% read rate
                read_at = format_timestamp(
                    datetime.fromisoformat(sent_at) + timedelta(hours=random.randint(1, 48))
                )
        
        # Determine related entity
        if 'page' in event_type:
            related_entity_type = 'page'
            related_entity_id = random.choice(list(pages.keys()))
        elif 'space' in event_type:
            related_entity_type = 'space'
            related_entity_id = random.choice(list(spaces.keys()))
        else:
            related_entity_type = random.choice(['page', 'space'])
            if related_entity_type == 'page':
                related_entity_id = random.choice(list(pages.keys()))
            else:
                related_entity_id = random.choice(list(spaces.keys()))
        
        message = f"{event_type.replace('_', ' ').title()}: {fake.sentence()}"
        
        notifications[str(notification_id)] = {
            "notification_id": str(notification_id),
            "recipient_user_id": random.choice(list(users.keys())),
            "event_type": event_type,
            "message": message,
            "related_entity_type": related_entity_type,
            "related_entity_id": related_entity_id,
            "sender_user_id": random.choice(list(users.keys())) if random.random() < 0.7 else None,
            "channel": random.choice(['system'] * 5 + ['email'] * 3 + ['web'] * 2),
            "delivery_status": delivery_status,
            "created_at": created_at,
            "sent_at": sent_at,
            "read_at": read_at
        }
        notification_id += 1
    
    return notifications

def save_to_json(data, filename, output_dir='data'):
    """Save data to JSON file in specified directory"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_dir) / filename
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  ✅ {filename}: {len(data)} records")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'data'
    output_dir.mkdir(exist_ok=True)
    output_dir = str(output_dir)
    
    print("\n" + "="*80)
    print("🎯 WIKI SEED DATA GENERATOR")
    print("="*80)
    print(f"\n📂 Output directory: {output_dir}")
    
    # Clean existing JSON files
    print("\n🗑️  Cleaning existing JSON files...")
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    if json_files:
        for json_file in json_files:
            os.remove(json_file)
        print(f"   Deleted {len(json_files)} existing JSON files")
    else:
        print("   No existing files to delete")
    
    print("\n📋 Generating wiki data...")
    
    # Generate in dependency order
    print("\n1. Users and Groups...")
    users = generate_users()
    groups = generate_groups()
    user_groups = generate_user_groups(users, groups)
    
    print("\n2. Spaces and Memberships...")
    spaces = generate_spaces(users)
    space_memberships = generate_space_memberships(users, spaces)
    space_features = generate_space_features(spaces)
    
    print("\n3. Pages and Versions...")
    pages = generate_pages(spaces, users)
    page_versions = generate_page_versions(pages, users)
    
    print("\n4. Permissions and Watchers...")
    permissions = generate_permissions(spaces, pages, users, groups)
    watchers = generate_watchers(spaces, pages, users, groups)
    
    print("\n5. System Operations...")
    export_jobs = generate_export_jobs(spaces, users)
    audit_logs = generate_audit_logs(users, spaces, pages)
    space_config_history = generate_space_config_history(spaces, users)
    
    print("\n6. Approvals and Notifications...")
    approval_requests = generate_approval_requests(pages, users)
    approval_decisions = generate_approval_decisions(approval_requests, users)
    notifications = generate_notifications(users, spaces, pages)
    
    # Save all data
    print("\n" + "="*80)
    print("💾 SAVING TO JSON FILES")
    print("="*80 + "\n")
    
    save_to_json(users, 'users.json', output_dir)
    save_to_json(groups, 'groups.json', output_dir)
    save_to_json(user_groups, 'user_groups.json', output_dir)
    save_to_json(spaces, 'spaces.json', output_dir)
    save_to_json(space_memberships, 'space_memberships.json', output_dir)
    save_to_json(space_features, 'space_features.json', output_dir)
    save_to_json(pages, 'pages.json', output_dir)
    save_to_json(page_versions, 'page_versions.json', output_dir)
    save_to_json(permissions, 'permissions.json', output_dir)
    save_to_json(watchers, 'watchers.json', output_dir)
    save_to_json(export_jobs, 'export_jobs.json', output_dir)
    save_to_json(audit_logs, 'audit_logs.json', output_dir)
    save_to_json(space_config_history, 'space_config_history.json', output_dir)
    save_to_json(approval_requests, 'approval_requests.json', output_dir)
    save_to_json(approval_decisions, 'approval_decisions.json', output_dir)
    save_to_json(notifications, 'notifications.json', output_dir)
    
    print("\n" + "="*80)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*80)
    
    total_records = (len(users) + len(groups) + len(user_groups) + 
                     len(spaces) + len(space_memberships) + len(space_features) +
                     len(pages) + len(page_versions) + len(permissions) + 
                     len(watchers) + len(export_jobs) + len(audit_logs) + 
                     len(space_config_history) + len(approval_requests) + 
                     len(approval_decisions) + len(notifications))
    
    print(f"\n📊 Summary: Generated {total_records:,} total records across 16 tables")
    print(f"   ✅ {len(users)} users with realistic role distribution")
    print(f"   ✅ {len(spaces)} spaces with hierarchical page structure")
    print(f"   ✅ {len(pages)} pages with version history")
    print(f"   ✅ Complete approval workflow with decisions")
    print(f"   ✅ Comprehensive permission and audit system")
    print(f"   ✅ All foreign key relationships maintained")
    print(f"   ✅ Consistent results with fixed seeds (42)")
    print(f"   ✅ Realistic data volumes for testing and development")
    print(f"   ✅ Metadata fields removed from approvals and notifications\n")

if __name__ == "__main__":
    main()