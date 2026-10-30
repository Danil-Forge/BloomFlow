from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .order import Order


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    provider_payment_id: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    idempotency_key: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        server_default=text("'RUB'"),
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default=text("'created'"),
    )

    payment_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "btrim(provider) <> ''",
            name="payments_provider_nonempty_chk",
        ),
        CheckConstraint(
            "amount > 0 AND amount <> 'NaN'::numeric",
            name="payments_amount_chk",
        ),
        CheckConstraint(
            "currency = 'RUB'",
            name="payments_currency_chk",
        ),
        CheckConstraint(
            "status IN ("
            "'created', 'pending', 'succeeded', "
            "'failed', 'canceled'"
            ")",
            name="payments_status_chk",
        ),
        CheckConstraint(
            "(status = 'succeeded') = (paid_at IS NOT NULL)",
            name="payments_paid_at_chk",
        ),
        UniqueConstraint(
            "provider",
            "provider_payment_id",
            name="payments_provider_payment_unique",
        ),
        Index(
            "payments_one_active_per_order_idx",
            "order_id",
            unique=True,
            postgresql_where=text(
                "status IN ('created', 'pending')"
            ),
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="payments",
    )


Index(
    "payments_order_created_idx",
    Payment.order_id,
    Payment.created_at.desc(),
    Payment.id.desc(),
)
