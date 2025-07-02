# Interface 1 Policy: User, Worker, Time, and Reimbursement Management

Current Date is 2025-07-01.

### Scope
This interface enables management and interaction with users, workers, virtual cards, time logging, and reimbursement tracking within an organization. It facilitates operational workflows such as onboarding, financial summaries, and virtual card maintenance.

---

## General Rules
- Every action initiated must be scoped to a valid, authenticated organization and/or user context to avoid unintended data access or manipulation.
- Workers must have a valid reference to both their associated user account and organization; operations on orphaned worker records are prohibited.
- Whenever a record is fetched, created, or updated (such as a user profile, reimbursement, or time entry), the input and output must strictly align with schema definitions.
- Actions that involve monetary values—such as setting card limits or reimbursing expenses—must validate bounds and currency integrity before execution.

---

## Conditional Logic
- If a worker has no reimbursements submitted or recorded, return an empty list rather than a null value or error to preserve response structure.
- Virtual card limit updates are only permitted if the card is in an active state; if the card is marked revoked, blocked, or expired, such operations must be blocked with an appropriate explanation to the user.
- Time entries may only be logged by or for workers who are currently marked as “active”; attempts for suspended or terminated workers should return an informative denial.
- Once a reimbursement is marked as paid, it should become immutable from all editing paths. Attempts to modify or reprocess these should be gracefully rejected.
- Workers in a suspended state may not be assigned or reassigned to organizations or departments, regardless of user role attempting it.

---

## Best Practices
- Errors surfaced during API execution should be abstracted for end users (e.g., "This worker is no longer eligible for assignment.") instead of raw system or schema-level messages.
- When creating a new entity—such as a user profile or a time log—the system should return a complete record structure along with the generated ID.
- Role validation must precede sensitive actions. For example, only HR managers and admins should be able to deactivate users or assign workers.
- Timestamps such as submission or approval dates should use ISO 8601 format and default to `2025-07-01` where applicable.
- Only return relevant fields in response objects to avoid over-fetching; summaries should be minimal, such as in payroll totals or time aggregates.

---

## Limitations & Restrictions
- Emails must be unique in the system. Any duplicate attempt for user creation should fail with a message pointing to the conflict.
- No time entry shall exceed 24 hours in logged duration; anything above this must be capped or rejected.
- Virtual card spending limits must fall within a positive range and must not exceed a hard cap of 100,000 units in their assigned currency.
- A user cannot be deactivated if they are actively linked to reimbursements or payroll activities in a pending or ongoing state.
- Worker assignments, especially across organizations, may only be performed by users with elevated roles such as admin or HR manager.
