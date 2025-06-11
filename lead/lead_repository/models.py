from sqlalchemy import String, Integer, Boolean

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class LeadModel(Base):
    __tablename__ = "lead"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Lead(id={self.id!r}, name={self.name!r}, first_name={self.first_name!r}, phone={self.phone!r}, email={self.email!r}, is_active={self.is_active!r}, adv_id={self.adv_id!r})"

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "phone": self.phone,
            "email": self.email,
            "adv_id": self.adv_id,
            "is_active": self.is_active,
            "is_archived": self.is_archived,
        }
