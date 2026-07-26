from __future__ import annotations

import enum
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Generator

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eulyonis.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class TransactionState(str, enum.Enum):
    DRAFT = "DRAFT"
    AUTHORIZED = "AUTHORIZED"
    SUBMITTED = "SUBMITTED"
    SETTLED = "SETTLED"
    RECONCILED = "RECONCILED"
    EXCEPTION = "EXCEPTION"
    REVERSED = "REVERSED"
    CANCELLED = "CANCELLED"


ALLOWED_TRANSITIONS: dict[TransactionState, set[TransactionState]] = {
    TransactionState.DRAFT: {TransactionState.AUTHORIZED, TransactionState.CANCELLED},
    TransactionState.AUTHORIZED: {TransactionState.SUBMITTED, TransactionState.CANCELLED},
    TransactionState.SUBMITTED: {TransactionState.SETTLED, TransactionState.EXCEPTION},
    TransactionState.SETTLED: {TransactionState.RECONCILED, TransactionState.EXCEPTION, TransactionState.REVERSED},
    TransactionState.EXCEPTION: {TransactionState.RECONCILED, TransactionState.CANCELLED},
    TransactionState.RECONCILED: {TransactionState.REVERSED},
    TransactionState.REVERSED: set(),
    TransactionState.CANCELLED: set(),
}


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(3))
    payer_ref: Mapped[str] = mapped_column(String(128))
    beneficiary_ref: Mapped[str] = mapped_column(String(128))
    purpose: Mapped[str] = mapped_column(String(64), default="GENERAL")
    state: Mapped[TransactionState] = mapped_column(Enum(TransactionState), default=TransactionState.DRAFT)
    rail_reference: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    evidence_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    audit_events: Mapped[list["AuditEvent"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    transaction_id: Mapped[str] = mapped_column(ForeignKey("transactions.id"), index=True)
    actor: Mapped[str] = mapped_column(String(128))
    event_type: Mapped[str] = mapped_column(String(64))
    previous_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    new_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    transaction: Mapped[Transaction] = relationship(back_populates="audit_events")


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    subject_ref: Mapped[str] = mapped_column(String(128), index=True)
    obligation_type: Mapped[str] = mapped_column(String(64))
    amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    channel: Mapped[str] = mapped_column(String(32), default="IN_APP")
    status: Mapped[str] = mapped_column(String(32), default="SCHEDULED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(engine)

app = FastAPI(
    title="EULYONIS Trust Core",
    version="0.1.0",
    description="Prototype-only canonical ledger, audit, reconciliation and intelligent reminder service.",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def record_audit(
    db: Session,
    tx: Transaction,
    actor: str,
    event_type: str,
    reason: str,
    previous_state: TransactionState | None = None,
    new_state: TransactionState | None = None,
) -> None:
    db.add(
        AuditEvent(
            id=str(uuid.uuid4()),
            transaction_id=tx.id,
            actor=actor,
            event_type=event_type,
            previous_state=previous_state.value if previous_state else None,
            new_state=new_state.value if new_state else None,
            reason=reason,
        )
    )


def transition(db: Session, tx: Transaction, target: TransactionState, actor: str, reason: str) -> Transaction:
    if target not in ALLOWED_TRANSITIONS[tx.state]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Transition {tx.state.value} -> {target.value} is not permitted",
        )
    previous = tx.state
    tx.state = target
    tx.updated_at = utcnow()
    record_audit(db, tx, actor, "STATE_TRANSITION", reason, previous, target)
    db.commit()
    db.refresh(tx)
    return tx


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    payer_ref: str = Field(min_length=1, max_length=128)
    beneficiary_ref: str = Field(min_length=1, max_length=128)
    purpose: str = Field(default="GENERAL", max_length=64)


class TransactionView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    idempotency_key: str
    amount: Decimal
    currency: str
    payer_ref: str
    beneficiary_ref: str
    purpose: str
    state: TransactionState
    rail_reference: str | None
    evidence_uri: str | None
    created_at: datetime
    updated_at: datetime


class SubmitRequest(BaseModel):
    rail_reference: str = Field(min_length=1, max_length=128)


class SettleRequest(BaseModel):
    evidence_uri: str | None = None


class ReconcileRequest(BaseModel):
    rail_reference: str
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)


class ReconcileResult(BaseModel):
    transaction_id: str
    result: str
    confidence: int
    factors: list[str]
    state: TransactionState


class ReminderCreate(BaseModel):
    subject_ref: str
    obligation_type: str
    due_at: datetime
    amount: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    channel: str = "IN_APP"


class ReminderView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    subject_ref: str
    obligation_type: str
    due_at: datetime
    amount: Decimal | None
    currency: str | None
    channel: str
    status: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "eulyonis-trust-core", "mode": "prototype"}


@app.post("/v1/transactions", response_model=TransactionView, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Header(default="demo-tenant", alias="X-Tenant-ID"),
    actor: str = Header(default="demo-user", alias="X-Actor-ID"),
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> Transaction:
    existing = db.scalar(select(Transaction).where(Transaction.idempotency_key == idempotency_key))
    if existing:
        return existing

    tx = Transaction(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        idempotency_key=idempotency_key,
        amount=payload.amount,
        currency=payload.currency.upper(),
        payer_ref=payload.payer_ref,
        beneficiary_ref=payload.beneficiary_ref,
        purpose=payload.purpose,
    )
    db.add(tx)
    db.flush()
    record_audit(db, tx, actor, "TRANSACTION_CREATED", "Transaction created in DRAFT state", None, TransactionState.DRAFT)
    db.commit()
    db.refresh(tx)
    return tx


def get_transaction_or_404(db: Session, transaction_id: str) -> Transaction:
    tx = db.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@app.get("/v1/transactions/{transaction_id}", response_model=TransactionView)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)) -> Transaction:
    return get_transaction_or_404(db, transaction_id)


@app.post("/v1/transactions/{transaction_id}/authorize", response_model=TransactionView)
def authorize_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    actor: str = Header(default="demo-approver", alias="X-Actor-ID"),
) -> Transaction:
    return transition(db, get_transaction_or_404(db, transaction_id), TransactionState.AUTHORIZED, actor, "Explicit user authorization")


@app.post("/v1/transactions/{transaction_id}/submit", response_model=TransactionView)
def submit_transaction(
    transaction_id: str,
    payload: SubmitRequest,
    db: Session = Depends(get_db),
    actor: str = Header(default="payment-orchestrator", alias="X-Actor-ID"),
) -> Transaction:
    tx = get_transaction_or_404(db, transaction_id)
    tx.rail_reference = payload.rail_reference
    return transition(db, tx, TransactionState.SUBMITTED, actor, "Submitted to simulated payment rail")


@app.post("/v1/transactions/{transaction_id}/settle", response_model=TransactionView)
def settle_transaction(
    transaction_id: str,
    payload: SettleRequest,
    db: Session = Depends(get_db),
    actor: str = Header(default="mock-rail", alias="X-Actor-ID"),
) -> Transaction:
    tx = get_transaction_or_404(db, transaction_id)
    tx.evidence_uri = payload.evidence_uri
    return transition(db, tx, TransactionState.SETTLED, actor, "Simulated rail confirmed settlement")


@app.post("/v1/transactions/{transaction_id}/reconcile", response_model=ReconcileResult)
def reconcile_transaction(
    transaction_id: str,
    payload: ReconcileRequest,
    db: Session = Depends(get_db),
    actor: str = Header(default="reconciliation-engine", alias="X-Actor-ID"),
) -> ReconcileResult:
    tx = get_transaction_or_404(db, transaction_id)
    if tx.state not in {TransactionState.SETTLED, TransactionState.EXCEPTION}:
        raise HTTPException(status_code=409, detail="Only SETTLED or EXCEPTION transactions may be reconciled")

    factors: list[str] = []
    exact = True
    if tx.rail_reference == payload.rail_reference:
        factors.append("rail_reference_exact")
    else:
        exact = False
        factors.append("rail_reference_mismatch")
    if tx.amount == payload.amount:
        factors.append("amount_exact")
    else:
        exact = False
        factors.append("amount_mismatch")
    if tx.currency == payload.currency.upper():
        factors.append("currency_exact")
    else:
        exact = False
        factors.append("currency_mismatch")

    target = TransactionState.RECONCILED if exact else TransactionState.EXCEPTION
    transition(db, tx, target, actor, "Deterministic reconciliation completed")
    return ReconcileResult(
        transaction_id=tx.id,
        result="MATCHED" if exact else "EXCEPTION",
        confidence=100 if exact else 25,
        factors=factors,
        state=tx.state,
    )


@app.post("/v1/reminders", response_model=ReminderView, status_code=status.HTTP_201_CREATED)
def create_reminder(
    payload: ReminderCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Header(default="demo-tenant", alias="X-Tenant-ID"),
) -> Reminder:
    reminder = Reminder(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        subject_ref=payload.subject_ref,
        obligation_type=payload.obligation_type,
        amount=payload.amount,
        currency=payload.currency.upper() if payload.currency else None,
        due_at=payload.due_at,
        channel=payload.channel,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@app.get("/v1/transactions/{transaction_id}/audit")
def get_audit(transaction_id: str, db: Session = Depends(get_db)) -> list[dict[str, str | None]]:
    get_transaction_or_404(db, transaction_id)
    events = db.scalars(
        select(AuditEvent).where(AuditEvent.transaction_id == transaction_id).order_by(AuditEvent.created_at)
    ).all()
    return [
        {
            "id": event.id,
            "actor": event.actor,
            "event_type": event.event_type,
            "previous_state": event.previous_state,
            "new_state": event.new_state,
            "reason": event.reason,
            "created_at": event.created_at.isoformat(),
        }
        for event in events
    ]
