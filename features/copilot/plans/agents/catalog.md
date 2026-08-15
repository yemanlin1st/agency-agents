# Agents Catalog — Canonical

This catalog lists the core agent templates designed to be specialized per domain using domain profiles.

Core agent templates:
- Data Ingest Agent
- Context Retriever Agent
- Model Ops Agent
- CI/CD Agent
- PR Triage / Code Review Agent
- Security Scanner Agent
- Incident Response Agent
- Business Rule Agent (policy-as-code enforcer)
- Product Spec & Roadmap Agent
- UX Research Agent
- Backend Builder Agent
- Frontend Builder Agent

Domain profiles (examples):
- fintech: KYC connectors, AML heuristics, PCI/AML policies
- medtech: FHIR/HL7 connectors, de-identification, HIPAA policies
- legaltech: contract clause ontology, chain-of-custody controls
- agritech: sensor & satellite connectors, traceability
- edutech: LMS connectors, FERPA controls
- transptech: telematics connectors, safety gating

For each agent template, see templates/agent-template.yaml for the configuration schema that must be used to create a domain-specialized agent instance.
