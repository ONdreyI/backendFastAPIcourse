import sys
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager  # noqa: E402
from src.app.hotels import router as hotel_router  # noga: E402
from src.app.auth import router as auth_router  # noga: E402
from src.app.rooms import router as room_router  # noga: E402
from src.app.bookings import router as bookings_router  # noga: E402
from src.app.facilities import router as facilities_router  # noga: E402
from src.config import settings  # noga: E402
from src.app.images import router as router_images  # noga: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


print(f"settings.DB_NAME={settings.DB_NAME}")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def func():
    return {"message": "Wellcome to the HOTELS!"}


app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
