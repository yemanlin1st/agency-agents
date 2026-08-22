# PEFY Agent Governance

This repository participates in the PEFY-GG sovereign agentic architecture. These instructions apply to every coding agent operating in this repository unless a more specific nested `AGENTS.md` imposes stricter rules.

## Architecture precedence

Use this order of authority when instructions or capabilities overlap:

1. **Owner / authorized executive decision**
2. **PEA sovereign orchestration and approved policy**
3. **PEFY-GG Ω INTERCORE 360™ operating blueprint**
4. **MƐTAPEFYON Ω™ / METAPEFYON OMEGA™ execution and intelligence fabric**
5. **PEFY-GG OMNIA Skillspector DeepSmart MCP™ registry and routing controls**
6. **AAOS-X command, control, execution, and resilience planes**
7. **PEFY Elite Execution Router / PEFY Agentic Dev Orchestrator**
8. Domain agents, agencies, skills, MCP servers, external providers, and project-local tooling

External providers such as 21st.dev are capabilities, not governance authorities.

## Default operating posture

- Read-only first.
- Sandbox-first for untrusted, generated, or experimental execution.
- PR-first for repository changes.
- Proof-first before completion claims.
- Cash-aware and cost-aware where model, cloud, or provider usage is metered.
- Minimal-context and minimal-agent routing by default.
- Prefer deterministic tools and existing repository assets before LLM generation.
- Do not create duplicate agents, registries, memories, routers, or design systems when an approved PEFY capability already covers the need.

## Approval boundary

Do not perform production write/delete, outbound send, payment, signature, identity/account-wide action, irreversible migration, privileged security change, or equivalent high-impact action without the required owner/policy approval, scoped authority, audit logging, rollback or recovery path, and verification evidence.

## PEA + councils/councillors

PEA is the sovereign orchestrator. Use the smallest review set appropriate to the risk. Relevant councils/councillors review architecture, security, compliance, legal/IP, data, finance, operations, brand/UX, or delivery quality when the change materially affects those domains.

Councils are reviewers and decision-support layers. They are not parallel authors of the same change unless PEA explicitly assigns separable workstreams.

## Capability routing

### PEFY Elite Execution Router

Use for normal task classification and minimum-specialist selection.

### PEFY Skill Intake Auditor

Use before admitting a new third-party skill, MCP server, agent pack, plugin, dependency, or agency into the approved fabric. Check provenance, license, permissions, data access, maintenance health, duplication, security, and rollback.

### OMNIA Branch-Swarm

Use for isolated parallel work only when workstreams are independent. Each worker uses its own branch/worktree or equivalent isolation boundary. Conflicting writes remain serialized.

### PEFY Agentic Dev Orchestrator

Use for software engineering delivery, including UI, architecture, backend, AI, data, security, DevSecOps, testing, documentation, and incident remediation.

### 21st.dev

Treat 21st.dev as an external UI acceleration capability for compatible React/Next.js/shadcn workflows. Search and reuse before generating. All imported/generated code remains subject to PEFY security, accessibility, performance, licensing, brand, test, and evidence gates.

## Memory and context

- Keep mission memory separate from raw conversational context.
- Persist only what must survive the current run and only to an approved store.
- Distill completed work before handoff.
- Do not duplicate the same context across multiple agents.
- Cache stable discovery results when safe.
- Treat experimental memory systems, including Claude-Mem pilots, as restricted until explicitly approved for the target environment.
- Never persist secrets, raw credentials, unnecessary personal data, or privileged tokens in agent memory.

## AAOS-X planes

Every non-trivial workflow should map to the following planes:

- **Command plane**: intent, authority, priority, approval.
- **Control plane**: policy, routing, identity, risk, budgets, rate limits.
- **Execution plane**: agents, skills, tools, MCPs, code, tests, deployments.
- **Resilience plane**: audit trail, backup, replica, replay, synchronization, rollback, recovery.

## Business-unit alignment

- **PEFY-TECH** owns and operates the development/AI engineering fabric.
- **PEFY-CYBER** is the cyber, assurance, resilience, and security-control extension.
- **PEFY-MANAGEMENT, PEFY-LANG, PEFY-TRAINING, PEFY-2COM, PEFY-COLISEUM, FYLAB, and Fondation Eulyson** consume capabilities through governed interfaces rather than maintaining separate duplicate agent fabrics.

Each strategic capability or platform must identify: owner/control layer, operator, risk owner, evidence owner, data classification, cyber/AI gate, revenue/cost model where applicable, and audit status.

## Completion contract

Every substantive output or change must make the following explicit when relevant:

- decision or result
- evidence
- owner or responsible layer
- risks/residual risks
- verification performed
- rollback/recovery path for risky changes
- next action

Never claim production-ready, compliant, secure, complete, or tested without corresponding evidence.