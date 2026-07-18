# Evaluation standard

Evaluate the graph, not only its prose.

Use representative tasks spanning read-only explanation, planning, investigation, ordinary implementation, high-risk change, independent review, verifier failure, and interrupted/resumed execution. Historical tasks may be replayed only after hiding the final solution from the acting agent.

Record:

- acceptance criteria satisfied;
- evidence correctness;
- unnecessary files or actions;
- required checks run;
- policy violations;
- human interventions;
- failure attribution;
- cost and latency when available;
- residual risk.

Do not collapse these into a fabricated universal score. Compare candidates with a transparent matrix and concrete failures.

A graph patch must state the observed failure, proposed structural change, expected effect, possible regressions, replay set, and rollback. Promote it only after validation and independent review.
