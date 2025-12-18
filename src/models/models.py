from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.db.base import Base
from src.models.enums import State


class SpyCat(Base): 
    __tablename__ = "spy_cat"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    years_of_experience: Mapped[int] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    fr_mission = relationship("Mission", back_populates="fr_spy_cat")


class Target(Base): 
    __tablename__ = "target"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True) 
    state: Mapped[State] = mapped_column(default=State.InProcess)

    fr_mission = relationship("Mission", back_populates="fr_target")


class Mission(Base): 
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    spy_cat: Mapped[int] = mapped_column(ForeignKey("spy_cat.id", ondelete="CASCADE"), nullable=True)
    target: Mapped[int] = mapped_column(ForeignKey("target.id"), nullable=False)
    state: Mapped[State] = mapped_column(default=State.InProcess)

    fr_spy_cat = relationship("SpyCat", back_populates="fr_mission")
    fr_target = relationship("Target", back_populates="fr_mission")
