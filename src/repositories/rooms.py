from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from backendCourse.src.models.rooms import RoomsOrm
from backendCourse.src.repositories.base import BaseRepository
from backendCourse.src.repositories.utils import rooms_ids_for_booking
from backendCourse.src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model)
            for model in result.unique().scalars().all()
        ]
