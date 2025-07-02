# Interface 3 Policy: Contracts, Invoices, Reimbursements, and Payroll Access

Current Date is 2025-07-01.

### Scope
This interface is responsible for managing and querying invoice statuses, payroll breakdowns, worker contracts, reimbursements, and virtual cards at an operational level.

---

## General Rules
- All operations must verify valid references to existing records including workers, contracts, invoices, and payments before proceeding.
- New invoices and reimbursements must not be created for terminated or suspended workers.
- Virtual cards may only be issued to active workers, and each card must link to a valid financial provider and user.
- All money-related changes must verify currency compatibility and fall within organizational financial policies.

---

## Conditional Logic
- Active workers must have both an active employment status and at least one ongoing contract with a status of active or signed.
- Contracts that are marked as ended or terminated should not be available for new invoice generation or editing.
- A reimbursement can only be processed if the worker is active and has an assigned user and organization.
- Payments used to mark invoices as paid must exist in the system and reference the invoice accurately; mismatched links should block the operation.
- Team assignment results must return a list, even if a worker has no team, to ensure consistent API behavior.

---

## Best Practices
- When creating new records like invoices, cards, or reimbursements, ensure complete detail is returned in the response.
- Provide clearly written messages if a request is blocked due to state mismatches (e.g. trying to pay a cancelled invoice).
- When summarizing payroll or contracts, break down items categorically for better readability.
- Use consistent ISO 8601 timestamps and apply `2025-07-01` as a static date where needed.
- Ensure each API describes input fields with purpose and constraints in `get_info()` for better interface understanding.

---

## Limitations & Restrictions
- Workers without any active contract should not appear in the list of active workers.
- Virtual cards cannot be reissued if a card already exists and is active for the same user.
- Invoices that are marked as paid or cancelled must not be modified again or re-paid.
- Contracts marked as ended or terminated cannot be extended or reactivated.
- Bank info updates must not overwrite currency unless explicitly required by policy or user instruction.
