# Evidence standard

Every material finding is one of:

- **fact** — directly supported by a file, commit, command, test, tool receipt, or user statement;
- **inference** — a reasoned conclusion from cited facts;
- **hypothesis** — a testable explanation not yet confirmed;
- **unknown** — evidence is unavailable or conflicting.

A finding records claim, class, evidence references, confidence as a qualitative label, limitations, and implication. Do not invent precision percentages.

Before history analysis, disclose shallow status, refs, commit range, and unavailable remotes. Co-change indicates correlation, not causation. Churn indicates change frequency, not poor quality. A revert-like message is a signal, not proof of failure.

Prefer primary repository evidence. Use external documentation for tool or framework behaviour, not to infer project intent. Secret-value content must never enter the evidence store.
