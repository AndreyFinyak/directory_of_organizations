from dependency_injector import containers, providers

from app.core.config import settings
from app.infrastructure.db.repository.repository import BaseRepository
from app.infrastructure.db.models import (
    Activity,
    Building,
    Organization,
    Phone,
)
from app.domain.dto import ActivityDTO, BuildingDTO, OrganizationDTO, PhoneDTO


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1",
        ]
    )

    activity_repository: providers.Factory[
        BaseRepository[Activity, ActivityDTO]
    ] = providers.Factory(
        BaseRepository,
        model=Activity,
    )
    building_repository: providers.Factory[
        BaseRepository[Building, BuildingDTO]
    ] = providers.Factory(
        BaseRepository,
        model=Building,
    )
    organization_repository: providers.Factory[
        BaseRepository[Organization, OrganizationDTO]
    ] = providers.Factory(
        BaseRepository,
        model=Organization,
    )
    phone_repository: providers.Factory[
        BaseRepository[Phone, PhoneDTO]
    ] = providers.Factory(
        BaseRepository,
        model=Phone,
    )
