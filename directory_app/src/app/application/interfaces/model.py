from typing import Protocol


class IModel(Protocol):
    def to_dto(self):
        pass
