from dataclasses import dataclass


@dataclass
class Organization:
    title: str
    id: int | None = None


@dataclass
class Building:
    address: str
    latitude: float
    longitude: float
    id: int | None = None


@dataclass
class Phone:
    number: str
    id: int | None = None


@dataclass
class Activity:
    name: str
    id: int | None = None
