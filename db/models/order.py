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
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .delivery import Delivery
    from .order_item import OrderItem
    from .payment import Payment
    from .user import User


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    checkout_key: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default=text("'awaiting_payment'"),
    )

    items_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    delivery_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    buyer_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    buyer_phone: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    payment_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
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
            "status IN ("
            "'awaiting_payment', "
            "'paid', "
            "'confirmed', "
            "'assembling', "
            "'delivering', "
            "'completed', "
            "'canceled'"
            ")",
            name="orders_status_valid_chk",
        ),
        CheckConstraint(
            "items_total > 0 AND items_total <> 'NaN'::numeric",
            name="orders_items_total_positive_chk",
        ),
        CheckConstraint(
            "delivery_price >= 0 AND delivery_price <> 'NaN'::numeric",
            name="orders_delivery_price_nonnegative_chk",
        ),
        CheckConstraint(
            "total_amount > 0 "
            "AND total_amount <> 'NaN'::numeric "
            "AND total_amount = items_total + delivery_price",
            name="orders_total_amount_valid_chk",
        ),
        CheckConstraint(
            "btrim(buyer_name) <> ''",
            name="orders_buyer_name_not_blank_chk",
        ),
        CheckConstraint(
            "btrim(buyer_phone) <> ''",
            name="orders_buyer_phone_not_blank_chk",
        ),
        CheckConstraint(
            "payment_expires_at > created_at",
            name="orders_payment_expires_after_created_chk",
        ),
    )

    user: Mapped["User"] = relationship(
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
    )

    delivery: Mapped["Delivery | None"] = relationship(
        back_populates="order",
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="order",
    )


Index(
    "orders_user_created_idx",
    Order.user_id,
    Order.created_at.desc(),
    Order.id.desc(),
)
