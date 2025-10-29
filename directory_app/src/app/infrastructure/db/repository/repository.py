
from typing import TypeVar, Generic, Type, Optional, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.model import IModel
from app.infrastructure.db.database import connection

ModelType = TypeVar("ModelType", bound=IModel)
DTOType = TypeVar("DTOType")


class BaseRepository(Generic[ModelType, DTOType]):
    model: Type[ModelType]

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @connection
    async def create(self, session: AsyncSession, dto: DTOType) -> DTOType:
        db_obj = self.model(**dto.__dict__)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj.to_dto()

    @connection
    async def get_by_id(
        self, session: AsyncSession, obj_id: int
    ) -> Optional[DTOType]:
        pk_field = self._get_pk_field()
        query = await session.execute(
            select(self.model).where(getattr(self.model, pk_field) == obj_id)
        )
        obj = query.scalar_one_or_none()
        return obj.to_dto() if obj else None

    @connection
    async def get_all(
        self, session: AsyncSession, limit: int = 100, offset: int = 0
    ) -> list[DTOType]:
        query = await (
            session.execute(select(self.model).limit(limit).offset(offset))
        )
        objs = query.scalars().all()
        return [obj.to_dto() for obj in objs]

    @connection
    async def filter_by(
        self, session: AsyncSession, **filters: Any
    ) -> list[DTOType]:
        query = await session.execute(select(self.model).filter_by(**filters))
        objs = query.scalars().all()
        return [obj.to_dto() for obj in objs]

    @connection
    async def update(
        self, session: AsyncSession, obj_id: int, **fields
    ) -> None:
        pk_field = self._get_pk_field()
        await session.execute(
            update(self.model)
            .where(getattr(self.model, pk_field) == obj_id)
            .values(**fields)
        )
        await session.commit()

    @connection
    async def delete(self, session: AsyncSession, obj_id: int) -> None:
        pk_field = self._get_pk_field()
        await session.execute(
            delete(self.model).where(getattr(self.model, pk_field) == obj_id)
        )
        await session.commit()

    def _get_pk_field(self) -> str:
        tablename = getattr(self.model, "__tablename__", None)
        if tablename:
            pk_field = f"{tablename[:-1]}_id"
            if hasattr(self.model, pk_field):
                return pk_field
        if hasattr(self.model, "id"):
            return "id"
        raise AttributeError(
            f"Cannot determine primary key field for model {self.model}"
        )
