from MySQLdb import _mysql



from Model import User

class UsersRepository:
    def __init__(self, db=_mysql.connect(host="127.0.0.1",user="c95gilles",
                  password="jcaxZYE6_3",database="filrougetest")):
        self._db = db

    async def get_all_users(
        self,
    ) -> User | None:
        customers = await ("SELECT user FROM filrougetest.user GROUP BY user)

        return customers(id=str(customers["id_Users"]), **customers) if customers else None
   

