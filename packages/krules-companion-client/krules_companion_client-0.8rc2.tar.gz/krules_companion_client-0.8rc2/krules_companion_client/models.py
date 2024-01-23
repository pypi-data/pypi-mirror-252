from enum import Enum


class EventType(str, Enum):
    EntityCreated = "io.krules.streams.entity.v1.created"
    EntityUpdated = "io.krules.streams.entity.v1.updated"
    EntityDeleted = "io.krules.streams.entity.v1.deleted"
    EntityCallback = "io.krules.streams.entity.v1.callback"
