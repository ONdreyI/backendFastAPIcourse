from datetime import date

from fastapi import APIRouter, Query, Body

from backendCourse.src.app.dependencies import PaginationDep, DBDep
from backendCourse.src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("", name="Получение списка отелей по сортировке")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location,
    #     title,
    # limit=per_page or 5,
    # offset=per_page * (pagination.page - 1),
    # )
    return await db.hotels.get_filtered_by_time(
        location,
        title,
        limit=per_page or 5,
        offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}", name="Получение одного отеля")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        return {"error": "Hotel not found"}
    return hotel


@router.post("", name="Add hotel data")
async def create_hotel(
    db: DBDep,
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
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "Ok", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await db.hotels.update(
        id=hotel_id,
        data=hotel_data,
    )
    await db.commit()
    return {"status": "updated"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно изменить только часть полей отеля</h1>",
)
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    await db.hotels.update(
        id=hotel_id,
        data=hotel_data,
        exclude_unset=True,
    )
    await db.commit()
    return {"status": "updated"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    await db.hotels.delete_data(id=hotel_id)
    await db.commit()
    return {"status": "deleted"}
