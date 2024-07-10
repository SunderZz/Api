from .schema import PreferenceshipBase, PreferenceshipIdBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import PreferenceshipRepository
from .services import create_preference_ship_service

router = APIRouter(tags=["preference_ship"])


@router.post(
    "/preference_ship/",
    status_code=status.HTTP_201_CREATED,
    response_model=PreferenceshipIdBase,
)
async def create_preference_ship(
    preference_ship: PreferenceshipBase,
    preference_ship_repository: PreferenceshipRepository = Depends(
        PreferenceshipRepository
    ),
    db: AsyncSession = Depends(get_db),
) -> PreferenceshipIdBase:
    return await create_preference_ship_service(
        preference_ship, preference_ship_repository, db
    )
