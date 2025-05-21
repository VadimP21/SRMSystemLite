from datetime import datetime, UTC
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r})"

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def formatted_price(self) -> str:
        """Возвращает цену в виде строки с валютой."""
        return f"${self.price:,.2f}"

    def description(self) -> str:
        """Возвращает полное описание продукта."""
        return f"Product Name: {self.name}, Price: {self.formatted_price()}"

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be non-negative")
        return value

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name must not be empty")
        return value
