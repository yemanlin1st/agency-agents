# PEFY Agentic Dev Fabric

## Purpose

PEFY Agentic Dev Fabric is an additive acceleration layer for software and AI delivery. It combines the existing Agency Agents catalog with 21st.dev UI retrieval and generation, deterministic tooling, minimal specialist routing, and production verification gates.

The objective is not to run the largest possible agent swarm. The objective is to reach a verified result with the smallest effective set of specialists, the smallest useful context, the fewest duplicated operations, and a clear evidence trail.

## Architecture

```text
User or product request
        |
        v
PEFY Agentic Dev Orchestrator
        |
        +--> classify task and risk
        |
        +--> select smallest specialist set
        |
        +--> reuse local code and approved registries
        |       |
        |       +--> 21st.dev for compatible React/shadcn UI
        |
        +--> parallel read-only discovery
        |
        +--> serialized implementation
        |
        +--> focused tests
        |
        +--> security / accessibility / performance review
        |
        +--> repository-wide required gates
        |
        v
Verified change + evidence + residual risk
```

## 21st.dev integration

21st.dev provides a unified MCP and CLI workflow for searching, installing, generating, iterating, and publishing React/shadcn-compatible components, themes, and templates.

PEFY uses 21st.dev as a reuse-first UI source. The orchestrator should search the registry before generating a new component when the target project is compatible.

### Supported bootstrap clients

The bootstrap script initializes 21st for detected supported clients:

- Codex
- Claude Code
- Cursor
- VS Code
- Windsurf

Agency Agents continues to support its broader set of targets, including OpenCode, OpenClaw, Gemini CLI, Copilot, Antigravity, Aider, Qwen, Codex, Cursor, Windsurf, and others supported by the native repository installer.

### Authentication

Use the environment variable:

```bash
export API_KEY_21ST="<your-runtime-secret>"
```

Never commit the secret to Git, dotfiles tracked by Git, CI logs, examples, screenshots, issue bodies, or documentation.

Alternatively, use the official interactive login locally:

```bash
21st login
```

The bootstrap intentionally refuses to pretend that authentication is complete when no credential is available.

## Installation

From the repository root:

```bash
bash scripts/install-pefy-dev-fabric.sh
```

To permit interactive 21st authentication during initialization:

```bash
PEFY_ALLOW_INTERACTIVE_AUTH=1 bash scripts/install-pefy-dev-fabric.sh
```

To initialize a client even when its executable is not detected:

```bash
PEFY_FORCE_21ST_CLIENTS=codex,claude bash scripts/install-pefy-dev-fabric.sh
```

To skip installing Agency Agents and only prepare 21st:

```bash
PEFY_INSTALL_AGENCY=0 bash scripts/install-pefy-dev-fabric.sh
```

## Required development capabilities

### 1. Product and UI

Core capabilities:
- frontend engineering
- UI design
- UX architecture
- design system integration
- accessibility
- internationalization
- responsive behavior
- performance and Core Web Vitals

Acceleration:
- local component reuse first
- 21st.dev search second
- generation only after reuse options are evaluated

### 2. Application architecture

Core capabilities:
- software architecture
- backend architecture
- API platform design
- domain boundaries
- distributed systems
- realtime collaboration when required
- migration and rollback planning

### 3. AI and agentic systems

Core capabilities:
- AI engineering
- multi-agent architecture
- prompt and instruction engineering
- RAG and retrieval
- evaluation
- tool design
- state and memory design
- approval gates
- auditability

Default agentic rule:
- start with one coordinator
- add specialists only for separable responsibilities
- define handoffs and state ownership
- narrow side effects
- cap retries and timeouts
- preserve an auditable execution trail

### 4. Security

Core capabilities:
- IAM
- secure sessions
- authorization
- code review
- dependency and supply-chain review
- network security
- incident response
- secrets management
- secure deployment and rollback

Mandatory rule:
- no secret is stored in source control

### 5. Data

Core capabilities:
- data engineering
- database design
- query optimization
- database reliability
- search relevance
- vector and RAG data paths where required

### 6. Platform and operations

Core capabilities:
- DevOps
- SRE
- observability
- CI/CD
- infrastructure automation
- FinOps
- capacity and reliability engineering

### 7. Quality

Core capabilities:
- focused tests before full suites
- code review
- minimal-diff discipline
- reproducible verification
- regression protection
- accessibility checks for UI
- performance checks for affected paths

## Fast execution policy

### Read once, reuse many

Avoid repeated scans of the same repository. Cache stable findings within the task and hand off compact summaries instead of full file dumps.

### Parallelize discovery, not conflicting writes

Run independent read-only checks concurrently. Examples include dependency inspection, static analysis, test discovery, documentation retrieval, and benchmark collection.

Serialize operations that can conflict, especially writes to the same files, migrations, secrets, deployment configuration, production changes, and merge operations.

### Prefer deterministic tools

Use linters, type checkers, unit tests, integration tests, schema validators, dependency scanners, and build tools instead of asking additional agents to reason about facts that tools can verify directly.

### Minimal context routing

Do not load every available skill or agent into every task. A large agent catalog is a capability inventory, not a default execution set.

### Minimal dependency growth

Before adding a new package, check whether the project, runtime, browser platform, framework, or existing dependencies already provide the required capability.

## Recommended routing examples

### Dashboard or application screen

1. PEFY Agentic Dev Orchestrator
2. UI Designer or UX Architect for interaction structure when needed
3. Frontend Developer
4. 21st.dev search and component retrieval
5. Accessibility specialist when the surface is material or regulated
6. Code Reviewer after implementation

### New AI workflow

1. PEFY Agentic Dev Orchestrator
2. AI Engineer
3. Multi-Agent Systems Architect only when multiple specialists are justified
4. RAG Pipeline Engineer when retrieval is part of the contract
5. Security review for tools, data boundaries, and secrets
6. Focused evals and runtime verification

### Production defect

1. PEFY Agentic Dev Orchestrator
2. Codebase Onboarding Engineer for unfamiliar repositories
3. Primary domain engineer
4. Minimal Change Engineer
5. Code Reviewer
6. Incident Response Commander only if the issue is operationally significant

## Performance KPIs

Recommended measurements:

| KPI | Direction |
| --- | --- |
| Request-to-verified-change lead time | decrease |
| First-pass CI success | increase |
| Escaped regressions | decrease |
| Duplicate repository scans | decrease |
| Agent handoffs per task | decrease unless complexity requires them |
| Mean context consumed per task | decrease |
| UI reuse from approved components | increase |
| Build and test duration | decrease without reducing coverage |
| Cost per verified task | decrease |
| Mean time to recovery | decrease |

## Security and governance controls

- secrets only through environment variables or approved secret managers
- least-privilege tool access
- explicit production approval boundaries
- auditable side effects
- dependency provenance review
- license review before third-party reuse
- test evidence before completion claims
- rollback path for production-affecting changes
- no automatic destructive action merely because an agent recommends it

## Current integration state

This repository branch adds:

1. `PEFY Agentic Dev Orchestrator` as a new engineering agent
2. `scripts/install-pefy-dev-fabric.sh` as the reusable bootstrap
3. this operating architecture and governance document
4. a CI smoke check for the bootstrap and orchestrator files

21st.dev runtime authentication remains intentionally external to Git. The integration becomes authenticated when `API_KEY_21ST` is provided in the shell or the official `21st login` flow is completed on the development machine.
