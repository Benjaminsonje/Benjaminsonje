from sqlalchemy import String, Integer, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    category = relationship("Category")