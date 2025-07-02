# Interface 5 Policy: Invoices, Reimbursements, Roles, and Worker Access Control

Current Date: 2025-07-01

---

## Scope and Responsibilities

This interface governs how organizations and administrators interact with invoices, reimbursements, user roles, time entries, and worker access control. It also provides workflows for team assignment, bonus logging, virtual card operations, and secure worker offboarding.

---

## General Operational Rules

- Every operation must validate the presence and correctness of referenced entities, such as workers, users, teams, cards, invoices, and reimbursements.
- Contracts, payroll items, and reimbursements must be tied to active, valid relationships between users, workers, and organizations.
- All financial transactions must be bounded within their contractual and temporal limits.

---

## Conditional Logic and Behavior

- If a user attempts to assign a worker to a team that does not belong to the same organization, the operation must be blocked and the user informed accordingly.
- When attempting to mark an invoice as paid, both the invoice and the payment must exist, and the payment must reference the correct invoice. Otherwise, the request is invalid.
- If a reimbursement is already in 'paid' status, it cannot be modified or updated in any way through this interface.
- Workers with active contracts or linked payroll entries cannot be removed from the system, even if deactivation is attempted.
- Virtual cards that are already revoked or expired cannot be reactivated or altered unless their status explicitly allows re-enablement.
- If a worker's system access is frozen, their user account must be moved to a 'suspended' status and all associated virtual cards blocked if they are still active.

---

## Best Practices and Recommendations

- Field-level validations should clearly indicate why an operation was denied or blocked. Use responses such as "Worker not found", "Card already revoked", or "Cannot remove worker with active payroll".
- Card status transitions should be controlled tightly: only 'blocked' or 'expired' cards can be re-enabled; 'revoked' cards are considered final and immutable.
- When creating contracts or logging bonuses, always associate them with the worker’s current active contract and organization. Avoid duplication.
- Document and reimbursement queries should return a sorted and filtered response, focusing on active records and recent dates.
- Ensure submitted dates (like contract start) and financial values (like bonus) are realistic and appropriately bounded. Amounts should be positive and within expected organizational policies.

---

## Security and Limitations

- Only authorized roles (e.g., admin or HR) may assign roles, create contracts, or adjust financial instruments such as payroll bonuses or invoice payments.
- Time entry queries across a period must be bound by a valid start and end date and should not exceed a full calendar year to limit over-fetching.
- No new contracts may be created for non-existent or offboarded workers.
- Role changes are not permitted for users in 'suspended' or 'inactive' state.
- Reimbursements and invoices cannot be linked to nonexistent workers or organizations, and any attempt must be gracefully rejected.