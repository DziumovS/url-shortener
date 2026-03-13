from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import engine
from src.database.models import Base
from src.exceptions import NoOriginalUrlFoundError, SlugAlreadyExistsError
from src.service import generate_short_url, get_url_by_slug
from src.dependencies import get_session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/c")
async def generate_slug(
    original_url: Annotated[str, Body(embed=True)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, str]:
    try:
        new_slug: str = await generate_short_url(original_url, session)
    except SlugAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate slug"
        ) from exc

    return {"data": new_slug}


@app.get("/g/{slug}")
async def get_short_url(
    slug: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RedirectResponse:
    try:
        original_url: str = await get_url_by_slug(slug, session)
    except NoOriginalUrlFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc

    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
