# HR Workforce Management Interface Policy

This interface governs the management of user identities, worker onboarding, position assignments, and organizational structure in a compliant and operationally sound manner. 

## Common Policy Rules

- All tools must verify the existence of referenced `user_id`, `organization_id`, or `position_id` before performing actions.
- Timestamps should be updated on modification actions.
- Enum values like `status`, `employment_type`, `role` should conform to schema-defined values.
- Actions such as termination, reassignment, and deactivation require strict validation with business reasoning provided by user or system.

## Worker-Specific Policy

- Workers can only belong to one organization at a time.
- Worker types must be either `employee` or `contractor`.
- Status changes must reflect HR policy: only `active` workers may be terminated or reassigned.
- Termination must record a `reason`, timestamp, and disable worker activity.

## Organization-Specific Policy

- Organizations must include valid country, timezone, and structured address.
- Updates to organizations should not violate existing worker associations unless explicitly allowed.

## Position and Department Management

- A user must have `manager`, `hr_manager`, or `admin` role to manage departments.
- Positions must follow employment type constraints and can only be assigned to valid workers.
- Department assignment requires unique ownership at a time and is tracked by audit.

## Escalation Policy

- Any user may escalate an issue via the `transfer_to_human_agents` tool, which logs and queues their request for review.
- Agents must have a human-readable issue summary to triage the case.
