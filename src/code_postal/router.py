import users.models as models
from typing import Annotated
from .schema import CodePostalBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import CodePostalRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["code_postal"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/code_postal/", status_code=status.HTTP_200_OK, response_model=list[CodePostalBase])
async def get_code_postal(code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),db: Session = Depends(get_db))-> list[CodePostalBase]:
    code_postal = await code_postal_repository.get_code_postal(db)
    code_postal_list = [model_to_dict(code) for code in code_postal]
    return [CodePostalBase(**code_postal_dict) for code_postal_dict in code_postal_list]


@router.get("/code_postal/{code_postal}", response_model=CodePostalBase)
async def get_code_postal_value(code_postal: str, code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db: Session = Depends(get_db)) -> CodePostalBase:
    value = await code_postal_repository.get_code_postal_query(db, code_postal)
    if value is None:
        raise HTTPException(status_code=404, detail="code_postal not found or attribute not found")
    code_postal_dict = model_to_dict(value)
        
    return CodePostalBase(**code_postal_dict)


@router.post("/code_postal/", status_code=status.HTTP_201_CREATED, response_model=CodePostalBase)
async def create_code_postal(code_postal: CodePostalBase,code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db: Session = Depends(get_db))-> CodePostalBase:
    new_code_postal = await code_postal_repository.create_code_postal(db, code_postal)
    code_postal_dict = model_to_dict(new_code_postal) 
    return CodePostalBase(**code_postal_dict)

@router.put("/code_postal/{code_postal_id}", status_code=status.HTTP_200_OK, response_model=CodePostalBase)
async def update_code_postal(code_postal_id: int, code_postal: CodePostalBase,code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db: Session = Depends(get_db))-> CodePostalBase:
    updated_code_postal = await code_postal_repository.update_code_postal(db, code_postal_id, code_postal)
    if updated_code_postal is None:
        raise HTTPException(status_code=404, detail="code_postal not found")
    code_postal_dict = model_to_dict(updated_code_postal) 
    return CodePostalBase(**code_postal_dict)