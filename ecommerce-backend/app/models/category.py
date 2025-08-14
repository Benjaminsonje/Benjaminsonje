from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)