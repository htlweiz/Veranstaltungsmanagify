from api.model import EventSchema, EventDB, EventPatch
from crud import events
from api.crud_router import CRUDRouter
from db.model import Event


class EventCRUDRouter(CRUDRouter[EventDB]):
    def __init__(self):
        super().__init__(Event.__tablename__, events.events, EventSchema, EventDB, EventPatch)


router = EventCRUDRouter()
