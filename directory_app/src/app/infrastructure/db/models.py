from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    SmallInteger,
    Float
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class Activity(Base):
    __tablename__ = "activities"

    activity_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True
    )
    level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, timezone=True, default=datetime.utcnow()
    )


class Building(Base):
    __tablename__ = "buildings"
    building_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(
            "buildings.building_id", ondelete="RESTRICT"
        ),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow()
    )

    building = relationship("Building", back_populates="organizations")


class Phone(Base):
    __tablename__ = "organization_phones"

    phone_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id = mapped_column(
        Integer,
        ForeignKey("organizations.organization_id", ondelete="CASCADE"),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
