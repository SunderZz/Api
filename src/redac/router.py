import redac.models as models
from .schema import RedactBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import RedactRepository
from .services import (
    get_redacts_service,
    get_redact_value_service,
    create_redact_service,
    update_redact_service
)

router = APIRouter(tags=["redact"])

@router.get("/redact/", status_code=status.HTTP_200_OK, response_model=list[RedactBase])
async def get_redacts(
    redact_repository: RedactRepository = Depends(RedactRepository),
    db: AsyncSession = Depends(get_db),
) -> list[RedactBase]:
    return await get_redacts_service(redact_repository, db)

@router.get("/redact/{redact_id}", response_model=RedactBase)
async def get_redact_value(
    admin_id: int,
    redact_id: int,
    redact_repository: RedactRepository = Depends(RedactRepository),
    db: AsyncSession = Depends(get_db),
) -> RedactBase:
    return await get_redact_value_service(admin_id, redact_id, redact_repository, db)

@router.post("/redact/", status_code=status.HTTP_201_CREATED, response_model=RedactBase)
async def create_redact(
    admin_id: int,
    redact_id: int,
    redact: RedactBase,
    redact_repository: RedactRepository = Depends(RedactRepository),
    db: AsyncSession = Depends(get_db),
) -> RedactBase:
    return await create_redact_service(admin_id, redact_id, redact, redact_repository, db)

@router.put(
    "/redact/{admin_id}/{recipe_id}",
    status_code=status.HTTP_200_OK,
    response_model=RedactBase,
)
async def update_redact(
    admin_id: int,
    recipe_id: int,
    redact: RedactBase,
    redact_repository: RedactRepository = Depends(RedactRepository),
    db: AsyncSession = Depends(get_db),
) -> RedactBase:
    return await update_redact_service(admin_id, recipe_id, redact, redact_repository, db)
