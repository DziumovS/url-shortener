from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.short_url_service import generate_short_url, get_url_by_slug
from src.api.deps import get_session
from src.exceptions.exceptions import SlugAlreadyExistsError, NoOriginalUrlFoundError
from src.schemas.url import URLInput


router = APIRouter()


@router.post("/c")
async def create_slug(
    data: URLInput = Body(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    try:
        new_slug: str = await generate_short_url(data.original_url, session)
    except SlugAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate slug"
        ) from exc
    return {"data": new_slug}


@router.get("/g/{slug}")
async def redirect_slug(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    try:
        original_url: str = await get_url_by_slug(slug, session)
    except NoOriginalUrlFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
