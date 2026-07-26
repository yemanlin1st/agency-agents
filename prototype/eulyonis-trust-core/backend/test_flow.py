from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_end_to_end_transaction_flow():
    create = client.post(
        "/v1/transactions",
        headers={"Idempotency-Key": "demo-key-001", "X-Tenant-ID": "pilot-lr"},
        json={
            "amount": "125.00",
            "currency": "LRD",
            "payer_ref": "merchant-001",
            "beneficiary_ref": "social-fund-001",
            "purpose": "SOCIAL_CONTRIBUTION",
        },
    )
    assert create.status_code == 201
    transaction = create.json()
    transaction_id = transaction["id"]
    assert transaction["state"] == "DRAFT"

    authorized = client.post(f"/v1/transactions/{transaction_id}/authorize")
    assert authorized.status_code == 200
    assert authorized.json()["state"] == "AUTHORIZED"

    submitted = client.post(
        f"/v1/transactions/{transaction_id}/submit",
        json={"rail_reference": "MOCK-RAIL-001"},
    )
    assert submitted.status_code == 200
    assert submitted.json()["state"] == "SUBMITTED"

    settled = client.post(
        f"/v1/transactions/{transaction_id}/settle",
        json={"evidence_uri": "evidence://mock-settlement/001"},
    )
    assert settled.status_code == 200
    assert settled.json()["state"] == "SETTLED"

    reconciled = client.post(
        f"/v1/transactions/{transaction_id}/reconcile",
        json={"rail_reference": "MOCK-RAIL-001", "amount": "125.00", "currency": "LRD"},
    )
    assert reconciled.status_code == 200
    assert reconciled.json()["result"] == "MATCHED"
    assert reconciled.json()["state"] == "RECONCILED"

    audit = client.get(f"/v1/transactions/{transaction_id}/audit")
    assert audit.status_code == 200
    assert len(audit.json()) >= 5
