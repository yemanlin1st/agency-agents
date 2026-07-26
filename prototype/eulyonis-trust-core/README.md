# EULYONIS Trust Core — Build Gate 1

Prototype-only foundation for EULYONIS Inclusive Economic Infrastructure™.

## Implemented in this gate

- canonical transaction ledger;
- controlled transaction state machine;
- idempotent transaction creation;
- explicit user authorization;
- simulated payment-rail submission and settlement;
- deterministic reconciliation;
- exception state for mismatches;
- immutable-style audit event history;
- social and statutory contribution reminder records;
- PostgreSQL deployment through Docker Compose;
- lightweight mobile-first demonstration interface;
- automated end-to-end smoke test.

## Regulatory and safety perimeter

This prototype:

- does not hold funds;
- does not connect to live payment systems;
- does not provide credit or insurance;
- uses simulated payment-rail references;
- must not contain real personal or financial data;
- requires explicit authorization before simulated submission;
- does not claim production readiness, certification or regulatory approval.

## Run

```bash
docker compose up --build
```

Open:

- Demo interface: `http://localhost:8080`
- API documentation: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/healthz`

## Run tests

```bash
cd backend
python -m pip install -r requirements.txt
pytest -q
```

## Demonstrated lifecycle

```text
DRAFT → AUTHORIZED → SUBMITTED → SETTLED → RECONCILED
                                      ↘ EXCEPTION
```

Every state transition records actor, previous state, new state, reason and timestamp.

## Next gate

Build Gate 2 should add:

1. tenant and user authentication;
2. purpose-based consent registry;
3. evidence object storage abstraction;
4. tolerance-based reconciliation;
5. configurable Country Pack rules;
6. notification delivery adapters;
7. offline queue and synchronization controls;
8. Merchant & SME Finance Lite and TontineTrust Lite bounded contexts.
