from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UserRepository:

    async def create_user(self, db: AsyncSession, f_name: str, name: str, mail: str, password: str):
        sql_call = text("CALL create_user(:f_name, :name, :mail, :password)")
        
        await db.execute(sql_call, {"f_name": f_name, "name": name, "mail": mail, "password": password})
        await db.commit()

#TODO
#         PUT
#         DELETE
#         POST
#         GET
