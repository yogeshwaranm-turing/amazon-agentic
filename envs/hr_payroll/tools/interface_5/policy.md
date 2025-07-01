# Interface 5: Financial Accounts & Identity Management Policy

This interface governs virtual card assignment, bank account linkage, and financial provider interaction.

- Users must have valid profiles to be linked with any financial instrument.
- Virtual cards must have defined limits and be linked to an active provider.
- Bank accounts must include holder name, account number, and associated provider.
- All updates must be confirmed and logged.

---

## Limitations
- Users may not have more than one active card per provider.
- Card limits and currency must align with organizational settings.
- Only users in `active` status may register or update financial records.
