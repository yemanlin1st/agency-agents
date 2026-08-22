# PEFY Account-Wide Agentic Alignment

## Purpose

This document aligns the PEFY Agentic Dev Fabric and 21st.dev integration with the existing PEFY-GG sovereign operating architecture. It prevents duplicate control planes, duplicate memory systems, uncontrolled agent proliferation, and tool-specific silos.

## Canonical architecture

```text
Owner / Executive Authority
        |
        v
PEA Sovereign Orchestrator
        |
        +-------------------------+
        |                         |
        v                         v
PEFY-GG Ω INTERCORE 360™      Councils / Councillors
Operating Blueprint           Risk & specialist review
        |
        v
MƐTAPEFYON Ω™
Sovereign Intelligence & Execution Fabric
        |
        v
PEFY-GG OMNIA Skillspector DeepSmart MCP™
Capability registry / discovery / routing / intake
        |
        +----------------------+----------------------+----------------------+
        |                      |                      |                      |
        v                      v                      v                      v
Elite Execution Router   Agentic Dev Orchestrator  Approved Agencies    MCP/Tool Layer
        |                      |                      |                      |
        +----------------------+----------------------+----------------------+
                               |
                               v
                     AAOS-X Execution Plane
                               |
                               v
                 Repositories / Apps / Platforms
                               |
                               v
                     Verification & Evidence
                               |
                               v
                     AAOS-X Resilience Plane
```

## Role of 21st.dev

21st.dev is classified as an **external UI capability provider**.

It is not:
- a replacement for MƐTAPEFYON Ω
- a replacement for OMNIA Skillspector
- a new sovereign orchestrator
- a new source of account-wide policy
- a reason to create a duplicate design system

It is used when a compatible application needs React/Next.js/shadcn components, templates, themes, or UI generation. The PEFY Agentic Dev Orchestrator invokes it through approved MCP/CLI paths after local reuse checks.

### 21st.dev control envelope

Before use:
1. Local component/design-system search.
2. Capability admission status from Skill Intake Auditor.
3. License/provenance/permission review as applicable.
4. Data classification check before sending any project context externally.

After use:
1. Adapt to PEFY/project design tokens.
2. Accessibility review.
3. Security and dependency review.
4. Performance review.
5. Tests and CI.
6. Evidence capture.

## Agent and agency alignment

### Do not multiply agents by default

The objective is capability coverage, not agent count. A new agent is justified only if at least one of these is true:
- it owns a distinct recurring decision domain
- it needs materially different tools or permissions
- it needs a separate evaluation harness
- it needs a distinct risk/approval boundary
- it reduces measurable delivery latency or error rate

Otherwise use an existing agent with a skill or tool.

### Existing workforce hierarchy

1. **PEA**: sovereign orchestration and escalation.
2. **PEFY Elite Execution Router**: initial task classification and route selection.
3. **PEFY Agentic Dev Orchestrator**: software delivery coordination.
4. **Specialist agents**: frontend, backend, architecture, AI, data, IAM, security, DevOps, SRE, QA, docs, etc.
5. **Specialist agencies**: grouped cross-functional capability when a multi-role outcome is required.
6. **Councils/councillors**: risk/quality/review layer, invoked selectively.

## AAOS-X mapping

| Plane | PEFY function | Examples |
|---|---|---|
| Command | intent, authority, prioritization | owner decision, PEA mission definition |
| Control | policy, route, identity, risk, budgets | OMNIA Skillspector, Elite Execution Router, approvals, model routing |
| Execution | task work | coding agents, 21st.dev, MCP servers, tests, CI/CD |
| Resilience | evidence and recovery | audit trail, backup, replay, rollback, synchronization |

## Business-unit ownership

### PEFY-TECH

Accountable owner/operator for:
- developer experience
- AI engineering fabric
- coding agents and engineering agencies
- MCP engineering layer
- CI/CD and developer tooling
- 21st.dev technical integration
- shared component and application engineering standards

### PEFY-CYBER

Assurance and risk-control extension for:
- identity and access
- secrets
- supply chain
- secure SDLC
- threat modeling
- security testing
- resilience
- production-change control

### Other BUs

PEFY-MANAGEMENT, PEFY-LANG, PEFY-TRAINING, PEFY-2COM, PEFY-COLISEUM, FYLAB, and Fondation Eulyson consume the shared fabric through domain-specific policies and skills. They should not fork a second general-purpose agent platform unless there is a documented sovereignty, regulatory, data-residency, or operational reason.

## Speed and efficiency architecture

### Fast path

```text
Request
  -> classify
  -> local instructions
  -> reuse existing assets
  -> choose 1 primary agent
  -> invoke only necessary tools/skills
  -> focused verification
  -> evidence
```

### Deep path

Triggered when architecture, security, compliance, financial impact, cross-BU impact, or high uncertainty exists.

```text
Request
  -> PEA / router
  -> architecture/risk decomposition
  -> isolated Branch-Swarm tracks
  -> specialist synthesis
  -> councils/councillors review
  -> controlled implementation
  -> full verification
  -> evidence + rollback
```

### Rules that improve latency

- one primary agent by default
- parallelize independent reads and tests, not conflicting writes
- distill context at handoffs
- avoid whole-repo scans when targeted retrieval is sufficient
- cache stable discoveries during the task
- use deterministic tools for deterministic work
- use the cheapest/fastest approved model that meets the quality/risk requirement
- escalate model capability only when verification or uncertainty warrants it
- use 21st.dev only after local reuse search for compatible UI tasks
- install new dependencies only when the existing stack cannot satisfy the requirement

## Memory architecture

Use a layered memory model:

1. **Ephemeral task context**: current reasoning inputs only.
2. **Mission memory**: compact state necessary for the active project/workstream.
3. **Approved durable knowledge**: validated architecture decisions, policies, schemas, runbooks, evaluations, and evidence.
4. **Restricted experiments**: memory tools that have not passed admission and privacy/security review.

Do not treat raw chat history as the canonical architecture store. Canonical decisions should be materialized into controlled artifacts and repositories.

## Capability intake gate

Every new agent, skill, MCP, framework, plugin, or external service should be scored against:

- business value
- capability uniqueness
- overlap/duplication
- latency benefit
- reliability
- security permissions
- data exposure
- license/IP
- maintenance health
- offline/self-hosting option where relevant
- interoperability
- observability
- reversibility
- cost
- evaluation evidence

Outcome:
- APPROVED
- APPROVED WITH RESTRICTIONS
- PILOT
- QUARANTINED
- REJECTED

## Required evidence for strategic platforms

Each strategic platform must record:
- owner/control layer
- operator
- risk owner
- evidence owner
- data classification
- cyber/AI gate status
- revenue/cost model where applicable
- audit status
- deployment state
- rollback/recovery mechanism

## Decision for this integration

**Decision:** retain the PEFY Agentic Dev Fabric as a subordinate engineering execution layer under the existing sovereign PEFY architecture. Integrate 21st.dev as an approved external UI capability, not as an independent platform.

**Owner:** PEFY-TECH.

**Risk/assurance extension:** PEFY-CYBER.

**Governance:** PEA + applicable councils/councillors.

**Default operating mode:** read-only first, sandbox-first, PR-first, proof-first.

**Next technical action:** enforce this hierarchy through root `AGENTS.md`, structured routing policy, CI validation, and project-level inheritance.