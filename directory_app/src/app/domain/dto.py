from datetime import datetime
from dataclasses import dataclass


@dataclass
class OrganizationDTO:
    title: str
    organization_id: int | None = None
    building_id: int | None = None
    created_at: datetime | None = None


@dataclass
class BuildingDTO:
    address: str
    latitude: float
    longitude: float
    building_id: int | None = None


@dataclass
class PhoneDTO:
    phone: str
    phone_id: int | None = None
    organization_id: int | None = None


@dataclass
class ActivityDTO:
    name: str
    id: int | None = None
    activity_id: int | None = None
    parent_id: int | None = None
    level: int | None = None
    created_at: datetime | None = None
