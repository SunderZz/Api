from sqlalchemy.orm import Session
from users_adresses.models import Users_adresses

def get_adress(db: Session, user_id: int, new_email: str)-> Users_adresses | None :
    db.execute("CALL update_user_email(:user_id, :new_email)", {"user_id": user_id, "new_email": new_email})
    db.commit()