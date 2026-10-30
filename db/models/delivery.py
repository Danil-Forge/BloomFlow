from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .order import Order


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )

    recipient_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    recipient_phone: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    address_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    delivery_window_start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    delivery_window_end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    courier_instructions: Mapped[str | None] = mapped_column(
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

    __table_args__ = (
        CheckConstraint(
            "btrim(recipient_name) <> ''",
            name="deliveries_recipient_name_not_blank_chk",
        ),
        CheckConstraint(
            "btrim(recipient_phone) <> ''",
            name="deliveries_recipient_phone_not_blank_chk",
        ),
        CheckConstraint(
            "btrim(address_text) <> ''",
            name="deliveries_address_not_blank_chk",
        ),
        CheckConstraint(
            "delivery_window_end_at > delivery_window_start_at",
            name="deliveries_window_valid_chk",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="delivery",
    )
