# Graph design standard

A valid graph has `id`, `version`, `runtime`, `entrypoints`, `nodes`, `edges`, and `invariants`.

## Nodes

Every node defines:

- `id`, `type`, and one-sentence purpose;
- named inputs and outputs;
- explicit context include/exclude lists;
- filesystem, command, network, Git, secret, and external-system permissions;
- a verifier and whether it blocks;
- bounded retry and termination;
- failure routes;
- whether human approval is required;
- expected evidence.

Allowed broad node classes:

- deterministic;
- retrieval;
- model;
- bounded-agent-loop;
- human-gate;
- terminal.

Do not use a persistent agent when a deterministic function or one constrained model call is sufficient.

## Edges

Each edge defines `from`, `to`, and an explicit condition. Mark cycles with `loop: true` and `max_iterations`. Reject cycles without a bound. A loop also needs a progress signal and a safe exit.

## Entry points

Expose user-level names such as `ask`, `plan`, `investigate`, `implement`, `review`, `verify`, and `evolve`. Entry points select paths; users should not operate internal node IDs.

## Permissions

Use least privilege. Avoid wildcard commands and unrestricted external systems. A graph may narrow host authority but cannot create authority. Any node that can merge, deploy, touch production data, reveal secrets, or perform another consequential external action requires explicit human approval.

## Verification

Prefer this hierarchy:

1. schema and deterministic constraints;
2. compiler, tests, static analysis, or executable receipts;
3. environment observation;
4. source-grounded checks;
5. independent model review;
6. human judgement.

The generator cannot be its own sole final reviewer for modifying work. Required verifiers block downstream edges.

## Candidate discipline

Always compare:

- minimal graph;
- recommended graph;
- frontier graph.

Select by evidence, not sophistication. Remove every node whose value cannot be explained by a real failure mode. Avoid fabricated composite scores; use a decision table with evidence, trade-offs, and unresolved uncertainty.

## Failure classes

Distinguish local, upstream, structural, environmental, policy, and budget failures. Route them differently. Do not retry semantic or policy failures as if they were transient timeouts.

## Completion

A terminal result includes outcome, artefacts, verification receipts, approvals, residual risk, unverified assumptions, and next user decision. “The model believes it is done” is not a completion criterion.
