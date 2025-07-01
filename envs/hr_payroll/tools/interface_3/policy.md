# Interface 3: Reimbursements & Time Tracking Policy

This interface helps manage reimbursements, log time entries, and monitor worker hours.

- Reimbursements must reference an active worker and must be submitted within 60 days of the transaction.
- Time entries must not exceed 16 hours per day and must not overlap existing entries.
- Only workers with active hourly contracts may submit time entries.
- All updates require user confirmation before being written to the system.

---

## Limitations
- You may not submit reimbursements for terminated or suspended workers.
- Time entries for future dates or overlapping hours must be rejected.
- Duration must match the time range if provided (start and end time).
