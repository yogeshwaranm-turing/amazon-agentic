from tau_bench.types import Action, Task

TEST = [
    Task(
        annotator="1",
        user_id="1",
        instruction=(
            "You are Danielle Johnson, a Global Administrator. You need to manage wiki operations and content. "
            "First, retrieve your user profile, then get details about the PROD space, create a new page in it, "
            "and grant permissions to another user."
        ),
        actions=[
            Action(name="get_user", kwargs={
                "user_id": "1"
            }),
            Action(name="get_space", kwargs={
                "space_id": "1"
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "Getting Started Guide",
                    "content_format": "markdown",
                    "state": "draft",
                    "created_by_user_id": "1"
                }
            }),
            Action(name="manage_permissions", kwargs={
                "action": "grant",
                "permission_data": {
                    "target_type": "page",
                    "target_id": "1",
                    "user_id": "6",
                    "permission_type": "edit"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="2",
        user_id="6",
        instruction=(
            "You are Jeffery Wagner, a Space Administrator. You need to manage content approval. "
            "Check your approval requests, then approve a pending page, and send a notification to the requester."
        ),
        actions=[
            Action(name="get_approval_requests", kwargs={
                "filter": "pending",
                "approver_user_id": "6"
            }),
            Action(name="decide_approval", kwargs={
                "request_id": "1",
                "decision_type": "approve",
                "decision_comment": "Looks good, approved for publication"
            }),
            Action(name="send_notification", kwargs={
                "user_id": "31",
                "notification_type": "approval",
                "message": "Your page has been approved and is ready for publication",
                "related_page_id": "5"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="3",
        user_id="31",
        instruction=(
            "You are Veronica Bowman, a Space Member. You need to work on wiki content. "
            "First, get the page you're working on, update its content, create a page version, "
            "and add yourself as a watcher."
        ),
        actions=[
            Action(name="get_page", kwargs={
                "page_id": "3"
            }),
            Action(name="manage_page", kwargs={
                "action": "update",
                "page_id": "3",
                "page_data": {
                    "state": "published",
                    "updated_by_user_id": "31"
                }
            }),
            Action(name="create_page_version", kwargs={
                "page_id": "3",
                "content": "# Architecture Overview\\n\\nThis document describes our system architecture...",
                "change_comment": "Initial architecture documentation",
                "created_by_user_id": "31"
            }),
            Action(name="manage_watchers", kwargs={
                "action": "add",
                "watcher_data": {
                    "user_id": "31",
                    "page_id": "3"
                }
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="4",
        user_id="181",
        instruction=(
            "You are Jessica Edwards, a Content Contributor. You need to export content and check audit logs. "
            "Create an export job for a space, then check your recent audit activities."
        ),
        actions=[
            Action(name="manage_exports", kwargs={
                "action": "create",
                "export_data": {
                    "space_id": "1",
                    "export_format": "pdf",
                    "requested_by_user_id": "181"
                }
            }),
            Action(name="get_audit_logs", kwargs={
                "filter": "user",
                "user_id": "181",
                "limit": 10
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="5",
        user_id="7",
        instruction=(
            "You are Anthony Gonzalez, a Space Administrator. You need to create a new space and configure it. "
            "Create a space, enable some features for it, add a member, and create an initial page."
        ),
        actions=[
            Action(name="manage_space", kwargs={
                "action": "create",
                "space_data": {
                    "space_key": "DOCS",
                    "space_name": "DOCS - Documentation Hub",
                    "space_purpose": "Central documentation repository",
                    "created_by_user_id": "7"
                }
            }),
            Action(name="manage_space_features", kwargs={
                "action": "enable",
                "space_id": "1",
                "feature_type": "page_templates"
            }),
            Action(name="manage_space_memberships", kwargs={
                "action": "add",
                "membership_data": {
                    "space_id": "1",
                    "user_id": "32",
                    "role": "contributor"
                }
            }),
            Action(name="manage_page", kwargs={
                "action": "create",
                "page_data": {
                    "space_id": "1",
                    "title": "Welcome to Documentation Hub",
                    "content_format": "markdown",
                    "state": "published",
                    "created_by_user_id": "7"
                }
            })
        ],
        outputs=[]
    )
]
