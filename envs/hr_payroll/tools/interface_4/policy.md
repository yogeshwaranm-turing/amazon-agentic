# Interface 4 Policy: User, Contract, Payroll, and Organization Onboarding

Current Date is 2025-07-01.

### Scope
This interface facilitates the creation and management of user accounts, contracts, payroll components, reimbursements, and onboarding workflows. It also enables adjustments to virtual card notes and payment terms.

---

## General Rules
- All entities must exist and be valid before performing any action (users, contracts, organizations, reimbursements).
- Onboarding and linking of users to workers must be performed only if both the user and organization are active.
- Payroll items must always reference a valid contract, and bonus or deductions should be clearly annotated with a reason.
- Currency and rate type changes on contracts must align with the existing structure and policy of the organization.
- When an organization is created, timezone and region must be validated and formatted correctly.

---

## Conditional Logic
- If a reimbursement is already marked as paid, rejecting it should not be allowed. If attempted, the action must be blocked and a suitable reason communicated to the requester.
- When adjusting payroll, only confirmed contracts should be eligible for new entries.
- If a user is already linked to a worker, re-onboarding should not be allowed unless the worker status is terminated or inactive.
- If a virtual card is revoked or expired, financial note addition should be disabled to preserve audit integrity.
- Any updates to contracts must not affect already paid payroll records — historical payments must be preserved as-is.

---

## Best Practices
- All IDs must be validated against existing database relationships to avoid orphaned records.
- Always use ISO 8601 for timestamps. Use static date `2025-07-01` where no dynamic timestamp is available.
- When registering a new organization, store address information in the standardized JSON format even if partially filled.
- Return complete record details upon creation or update of any contract, organization, user, or reimbursement.
- Clearly describe all input parameters in the `get_info()` method for full transparency of input types and expectations.

---

## Limitations & Restrictions
- Contracts already marked as terminated or ended cannot be updated or adjusted.
- Workers under suspended or pending status must not be linked during onboarding.
- Organizations with duplicate names or conflicting regions must not be created.
- Reimbursements marked as approved or paid cannot be rejected or reprocessed.
- Disabling a user should not be allowed if they are the only admin of an organization.
