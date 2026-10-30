
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(Base):
    __tablename__ = "order_items"

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

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )

    product_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    product_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    product_composition: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "btrim(product_name) <> ''",
            name="order_items_product_name_not_blank_chk",
        ),
        CheckConstraint(
            "btrim(product_description) <> ''",
            name="order_items_product_description_not_blank_chk",
        ),
        CheckConstraint(
            "unit_price > 0 "
            "AND unit_price <> 'NaN'::numeric",
            name="order_items_unit_price_positive_chk",
        ),
        CheckConstraint(
            "quantity > 0",
            name="order_items_quantity_positive_chk",
        ),
        CheckConstraint(
            "line_total > 0 "
            "AND line_total <> 'NaN'::numeric "
            "AND line_total = unit_price * quantity",
            name="order_items_line_total_valid_chk",
        ),
        UniqueConstraint(
            "order_id",
            "product_id",
            name="order_items_order_product_uq",
        ),
        Index(
            "order_items_product_id_idx",
            "product_id",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )