from datetime import datetime

from app.domain.dto import ActivityDTO, BuildingDTO, OrganizationDTO, PhoneDTO

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

    def to_dto(self) -> ActivityDTO:
        return ActivityDTO(
            activity_id=self.activity_id,
            name=self.name,
            parent_id=self.parent_id,
            level=self.level,
            created_at=self.created_at,
        )


class Building(Base):
    __tablename__ = "buildings"
    building_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    def to_dto(self) -> BuildingDTO:
        return BuildingDTO(
            building_id=self.building_id,
            address=self.address,
            latitude=self.latitude,
            longitude=self.longitude,
        )


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

    def to_dto(self) -> OrganizationDTO:
        return OrganizationDTO(
            organization_id=self.organization_id,
            title=self.title,
            building_id=self.building_id,
            created_at=self.created_at,
        )


class Phone(Base):
    __tablename__ = "organization_phones"

    phone_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id = mapped_column(
        Integer,
        ForeignKey("organizations.organization_id", ondelete="CASCADE"),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(String(50), nullable=False)

    def to_dto(self) -> PhoneDTO:
        return PhoneDTO(
            phone_id=self.phone_id,
            organization_id=self.organization_id,
            phone=self.phone,
        )
