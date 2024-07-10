from datetime import datetime as date_ts
import datetime
import re
import jwt

SECRET_KEY = "JWT"
ALGORITHM = "HS256"


def generate_token(user_id):
    payload = {
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        "sub": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def model_to_dict(model):
    return {c.key: getattr(model, c.key) for c in model.__mapper__.column_attrs}


def validate_password(password: str) -> bool:
    if not re.search(r"[A-Z]", password):
        return False
    if len(re.findall(r"[0-9]", password)) < 2:
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return True


def get_actual_ts():
    Timestamp = date_ts.now().isoformat()
    given_date_exact = date_ts.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    return given_date_exact
