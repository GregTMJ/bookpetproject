from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped

from src.db.configs import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    password: Mapped[str] = Column(String(255))
    name: Mapped[str] = Column(String(255))
    family_name: Mapped[str] = Column(String(255))
    username: Mapped[str] = Column(String(255), unique=True)
    active: Mapped[bool] = Column(Boolean, default=True)
