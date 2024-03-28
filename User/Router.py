# from fastapi import FastAPI, APIRouter

# app = FastAPI()

# router = APIRouter(tags=["user"])
# @router.get(
#     "/api/users",
#     dependencies=[Depends(have_role(DUTIES_READ_ROLES))],
#     responses={
#         **HTTPError401Exception.response_model(),
#     },
#     response_model=list[],
#     summary="Get list of duties.",
#     description=f"""
# Get duties data
# * Users allowed to call this endpoint : {', '.join(DUTIES_READ_ROLES)}.
# """,
#     tags=["v3"],
# )
# async def find_v3(
#     group_id: str,
#     anonymized: bool | None = None,
#     limit: int = 0,
#     sort: Annotated[
#         DutySorting | None,
#         Query(
#             description="""
#                  Sort the duties by the given criteria.
#                   Expects a criteria of the form `field:order` where
#                   field is the `field` to sort by, and `order` either
#                   `asc` or `desc`. For the time being, the only supported
#                   `field` is `check_in`"""
#         ),
#     ] = None,
#     start_date: Annotated[
#         str | None,
#         Query(
#             description="Filter on a start date, in GTFS format.",
#             examples=["20180224"],
#             pattern=r"^\d{4}\d{2}\d{2}$",
#         ),
#     ] = None,
#     duty_repository: DutyRepository = Depends(get_duty_repository),
# ) -> list[DutySchemaV3]:
#     match sort:
#         case None:
#             sort_check_in_desc = None
#         case DutySorting.CHECK_IN_ASC:
#             sort_check_in_desc = False
#         case DutySorting.CHECK_IN_DESC:
#             sort_check_in_desc = True

#     return [
#         DutySchemaV3.from_model(duty)
#         for duty in await duty_repository.find_anonymized(
#             group_id, limit, sort_check_in_desc, anonymized, start_date
#         )
#     ]
