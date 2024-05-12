from sqlalchemy.orm import Session
from .models import Given

class GivenRepository:

    async def create_given(self,db: Session, given: Given)->Given:
        db_given = Given(**given.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_given(self,db: Session)->Given:
        return db.query(Given).all()

    async def get_given_by_id(self,db: Session, id: int)->Given:
        return db.query(Given).filter(Given.Id_Notice == id).first()

    async def update_given(self,db: Session, id: int, given: Given)->Given:
        db_given = db.query(Given).filter(Given.Id_Notice == id).first()
        for key, value in given.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
