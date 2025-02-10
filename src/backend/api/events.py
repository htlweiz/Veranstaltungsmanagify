from typing import Coroutine, Any, List
from sqlalchemy.sql import and_
from api.model import EventSchema, EventDB, EventPatch
from crud import events
from api.crud_router import CRUDRouter, paginate
from db.model import Event, UserApproveEvent
from db.session import session


class EventCRUDRouter(CRUDRouter[EventDB]):
    def __init__(self):
        super().__init__(Event.__tablename__, events.events, EventSchema, EventDB, EventPatch)
    
    async def read(self, filter: events.BaseModel) -> List[EventDB]:
        query = self.crud_model.read(filter)
        query = paginate(query, filter)
        response = session.execute(query).scalars().all()

        for event in response:
            pending_approval = session.query(UserApproveEvent).where(and_(UserApproveEvent.event_id == event.event_id, UserApproveEvent.is_approved == False)).all()
            event.pending_approval = pending_approval
        return response


router = EventCRUDRouter()
