from datetime import datetime, UTC
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, Integer

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    validates,
)


class Base(DeclarativeBase):
    pass


class AdvModel(Base):
    __tablename__ = "adv"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    chanel: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Advertisement(id={self.id!r}, name={self.name!r}, cost={self.cost!r}, chanel={self.chanel!r}, created_at={self.created_at!r})"

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost": str(self.cost),
            "chanel": self.chanel,
            "created_at": self.created_at,
            "product_id": self.product_id,
        }

    def formatted_cost(self) -> str:
        """Возвращает цену в виде строки с валютой."""
        return f"${self.cost:,.2f}"

    def description(self) -> str:
        """Возвращает полное описание."""
        return f"Advertisement Name: {self.name}, Cost: {self.formatted_cost()}"

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
