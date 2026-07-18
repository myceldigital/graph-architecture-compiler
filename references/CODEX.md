# Codex execution protocol

## Capability detection

At the start identify the available surface: Codex app, CLI, IDE, cloud task, local checkout, remote devbox, GitHub connector, worktree support, subagent support, browser/computer use, and network policy.

Do not assume every surface exposes the same programmable subagent API. Preserve the same semantic graph in two modes:

- parallel mode for independent agents and isolated worktrees;
- sequential mode that writes each specialist output before the next pass.

## Task packet

Every delegated pass includes:

- task ID and role;
- objective;
- required inputs and evidence scope;
- read and write boundaries;
- allowed tools and commands;
- prohibited actions;
- output schema;
- acceptance criteria;
- maximum turns or attempts;
- stop conditions.

Personas without distinct contracts are not specialists.

## Everyday operation

1. Validate `.graph-architecture/graph.json`.
2. Map the user request to a named entrypoint.
3. Start a run record.
4. Load only the context projected for the ready node.
5. Execute with the node's permissions and bounds.
6. Run the blocking verifier.
7. Record concise evidence and state.
8. Follow the permitted edge or pause at a human gate.
9. Finish with receipts, residual risk, and next decision.

Natural-language steering can narrow scope, forbid an action, select a candidate, add review, or pause. Convert durable user preferences into an explicit policy diff; do not rely only on conversational memory.

## Modifying work

Use an isolated worktree where supported. The implementation pass gets the approved plan and scoped context. Independent review gets the task contract, final diff, project invariants, and test evidence—but not the implementer's persuasive rationale.

For frontend work, add browser verification when available. For infrastructure, migrations, auth, billing, clinical logic, or other high-risk areas, use repository-specific checks and human gates.

## GitHub delivery

Prefer a draft PR. Include goal, scope, architecture context, meaningful changes, checks, graph path, risk, unverified assumptions, and human review points. Do not merge unless the user explicitly requests it and policy permits it.
