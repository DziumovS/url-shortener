from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse

from database.database import engine
from database.models import Base
from exceptions import NoOriginalUrlFoundError
from service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_slug(
    original_url: str = Body(embed=True)
):
    new_slug = await generate_short_url(original_url)

    return {"data": new_slug}


@app.get("/{slug}")
async def get_short_url(slug: str):
    try:
        original_url = await get_url_by_slug(slug)
    except NoOriginalUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
