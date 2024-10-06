from backendCourse.src.repositories.bookings import BookingsRepository
from backendCourse.src.repositories.facilities import (
    FacilitiesRepository,
    RoomsFacilitiesRepository,
)
from backendCourse.src.repositories.hotels import HotelsRepository
from backendCourse.src.repositories.rooms import RoomsRepository
from backendCourse.src.repositories.users import UsersRepository


class DBManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
