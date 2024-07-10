from sqlalchemy.ext.asyncio import AsyncSession
from .repository import PreferenceshipRepository
from .schema import PreferenceshipBase, PreferenceshipIdBase
from common import model_to_dict


async def create_preference_ship_service(
    preference_ship: PreferenceshipBase,
    preference_ship_repository: PreferenceshipRepository,
    db: AsyncSession,
) -> PreferenceshipIdBase:
    new_preference_ship = await preference_ship_repository.create_preferenceship(
        db, preference_ship
    )
    preference_ship_dict = model_to_dict(new_preference_ship)
    return PreferenceshipIdBase(**preference_ship_dict)
