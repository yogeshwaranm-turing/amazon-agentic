# Policy: Invoices, Reimbursements, Roles, and Worker Access Control

**Effective Date: July 1, 2025**

---

### Overview

This policy governs how organizations and administrators manage invoices, reimbursements, user roles, time entries, and worker access control. It also supports workflows related to team assignments, bonus logging, virtual card operations, and secure worker offboarding. All operations must respect organizational boundaries and user permissions.

---

### General Operational Rules

- The system must validate the presence and correctness of referenced entities—including workers, users, teams, cards, invoices, and reimbursements—before performing any operation.

- Contracts, payroll items, and reimbursements must be associated with active, valid relationships between users, workers, and organizations.

- All financial transactions must fall within the contractual and temporal limits defined for those relationships. The system should enforce these boundaries to maintain financial control.

---

### Conditional Logic and Behavior

- If a user attempts to assign a worker to a team outside the same organization, the system must block the operation and return a clear explanation.

- When marking an invoice as paid, the system must ensure both the invoice and the payment exist, and that the payment properly references the invoice. If not, the operation must be rejected.

- Reimbursements in ‘paid’ status must not be modified or updated. These records are considered final and should be treated as immutable.

- Workers who have active contracts or are linked to payroll entries must not be removed from the system. Any removal or deactivation attempt should be denied until those connections are resolved.

- Virtual cards that are already marked as revoked or expired must not be reactivated unless their status explicitly permits re-enablement.

- If a worker’s access is frozen, their user account must be transitioned to ‘suspended’ status, and any active virtual cards associated with them must be blocked.

---

### Best Practices and Recommendations

- Field-level validations should provide specific, user-readable messages explaining why an operation was denied—for example: “Worker not found,” “Card already revoked,” or “Cannot remove worker with active payroll.”

- Virtual card status transitions should be strictly enforced. Only cards in ‘blocked’ or ‘expired’ status may be re-enabled. Cards marked as ‘revoked’ are permanent and must remain unchanged.

- When creating contracts or logging bonuses, these actions must reference the worker’s current active contract and organization. The system should prevent any duplication or cross-linking errors.

- Document and reimbursement queries should return sorted and filtered results focused on active records and recent entries to enhance clarity and relevance.

- Submitted values—such as start dates and financial amounts—must be realistic, positive, and fall within organizational policy thresholds.

---

### Security and Limitations

- Only users with authorized roles (e.g., HR or admin) may assign user roles, create contracts, or update financial records such as bonuses or invoice payments.

- Time entry queries must include valid start and end dates and should not span more than one calendar year to prevent over-fetching.

- Contracts must not be created for users who are offboarded or do not exist in the system.

- Users marked as ‘suspended’ or ‘inactive’ must not undergo any role changes.

- Reimbursements and invoices must not be linked to non-existent workers or organizations. Any such attempts must be rejected with a clear error message.
