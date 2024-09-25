from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, or_, func
from backendCourse.src.app.dependencies import PaginationDep
from backendCourse.src.schemas.hotels import HotelAdd, HotelPATCH

from src.database import async_session_maker

from src.models.hotels import HotelsOrm

from src.database import engine

from backendCourse.repositories.hotels import HotelsRepository

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", name="Получение списка отелей по сортировке")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location,
            title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1),
        )


@router.get("/{hotel_id}", name="Получение одного отеля")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            return {"error": "Hotel not found"}
        return hotel


@router.post("", name="Add hotel data")
async def create_hotel(
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Sochi Hotel",
                    "location": "Sochi city, Mira st. 5",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Dubai Hotel",
                    "location": "Sheikh Zayed Road Dubai, United Arab Emirates",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "Ok", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(
            id=hotel_id,
            data=hotel_data,
        )
        await session.commit()
        return {"status": "updated"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно изменить только часть полей отеля</h1>",
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(
            id=hotel_id,
            data=hotel_data,
            exclude_unset=True,
        )
        await session.commit()
        return {"status": "updated"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete_data(id=hotel_id)
        await session.commit()
        return {"status": "deleted"}
