from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UserRepository:

    async def create_user(self, db: AsyncSession, f_name: str, name: str, mail: str, password: str):
        sql_call = text("CALL create_user(:f_name, :name, :mail, :password)")
        
        await db.execute(sql_call, {"f_name": f_name, "name": name, "mail": mail, "password": password})
        await db.commit()

#TODO
#         PUT MODIFY USER
#         GET USER
#         PUT BLOCK USER FOR USER

# CREATE OR REPLACE PROCEDURE create_user(
#     p_f_name TEXT,
#     p_name TEXT,
#     p_mail TEXT,
#     p_password TEXT
# )
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     INSERT INTO users (f_name, name, mail, password, creation_date, modification_date, active)
#     VALUES (p_f_name, p_name, p_mail, crypt(p_password, gen_salt('bf')), NOW(), NOW(), TRUE);
# END;
# $$;

