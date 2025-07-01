# Interface 2: Payroll & Payment Processing Policy

This interface handles payroll calculations, payroll run management, invoice generation, and payment processing.

- Before initiating a payroll run, validate the organization, payroll period, and worker eligibility.
- A worker must have an active contract and valid time entries (if hourly) to be included.
- Show all calculated payroll items and wait for confirmation before finalizing.
- Invoices must be linked to a payroll run and organization pair.
- Payments must be linked to a payroll item, invoice, or reimbursement.
- Only one payment action is allowed per call and must be confirmed with the user.

---

## Limitations
- You may not initiate overlapping payroll runs for the same organization.
- Payments with inactive or missing bank/card information are disallowed.
- Invoice status must be `issued` before marking a payment as `completed`.
