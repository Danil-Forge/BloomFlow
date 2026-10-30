from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Numeric,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .cart_item import CartItem
    from .category import Category
    from .order_item import OrderItem
    from .product_image import ProductImage


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    composition: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        server_default=text("false"),
    )
    is_available: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        server_default=text("false"),
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
            "btrim(name) <> ''",
            name="products_name_not_blank_chk",
        ),
        CheckConstraint(
            "btrim(description) <> ''",
            name="products_description_not_blank_chk",
        ),
        CheckConstraint(
            "price > 0 AND price <> 'NaN'::numeric", name="products_price_positive_chk"
        ),
        CheckConstraint(
            "NOT is_available OR is_active",
            name="products_available_requires_active_chk",
        ),
        Index("products_category_id_idx", "category_id"),
    )

    category: Mapped["Category"] = relationship(
        back_populates="products",
    )

    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
