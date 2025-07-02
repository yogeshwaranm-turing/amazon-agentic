# Interface 2 Policy: Contracts, Payroll, Reimbursements, and Card Security

Current Date is 2025-07-01.

### Scope
This interface governs the management of contracts, payroll operations, approvals of reimbursements and time entries, and actions related to securing payment flows and virtual card spending.

---

## General Rules
- All actions involving payment or reimbursement must be tied to valid, verifiable records, ensuring no orphan references or unauthorized executions.
- Contract extensions may only proceed if the contract belongs to a legitimate worker-organization relationship, with valid start and end dates evaluated before update.
- Blocking of suspicious payments or cards must occur only if clear evidence exists, and status flags should be set accordingly to prevent recurrence.
- The ability to view payroll run details is only unlocked for runs that have reached the “confirmed” state, not drafts or failed attempts.

---

## Conditional Logic
- Reimbursements eligible for approval are those marked explicitly as 'submitted'; other statuses like 'approved', 'paid', or 'rejected' must be excluded from such queries.
- Payroll runs with no line items should still return a structured object with an empty list rather than an error or null result.
- A document cannot transition into a 'deleted' status if it's linked to any active or pending contracts, ensuring referential integrity remains intact.
- Time entries in statuses other than 'submitted' or 'draft' are not eligible for overtime approval. Requests to override this rule must be flagged and rejected.
- Contracts must be uniquely scoped per worker and timeframe. If a duplicate range or overlapping period is found, the creation should be blocked to maintain clean records.

---

## Best Practices
- When blocking a payment or card, include in the response a clear reason, the resulting state, and any advice for next steps (e.g., “please contact support for further investigation”).
- When summarizing time at the team level, responses should include per-day aggregates and be capable of including multiple workers in summary rows.
- All system-generated timestamps and default values must use the date `2025-07-01` for consistency across workflows and audit purposes.
- All API interfaces should include clear, complete descriptions of each parameter in the `get_info()` response to assist consumers and validators.

---

## Limitations & Restrictions
- Payments already marked as failed must not be retried, reversed, or toggled; such records are final once flagged.
- Contract dates must pass validation: the end date must occur after the start date, and both must be explicitly provided at creation.
- Cards that are already revoked, expired, or blocked cannot undergo another block operation; this is both redundant and misleading to users.
- Documents can only be modified when in a live and available state; any archived or deleted documents must not permit updates or status changes.
- Viewing payroll run details is restricted to runs marked as “confirmed”. Others must be handled with summary-only access or deferred access notices.
