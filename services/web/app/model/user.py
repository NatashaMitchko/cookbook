import bcrypt
import json
import uuid
from flask_login import UserMixin

from app import redis_client


class User(UserMixin):
    def __init__(self, id: str, username: str) -> None:
        self.id = id
        self.username = username


def user_limit_reached():
    """
    Only one user allowed, and that user is **me**
    """
    _, keys = redis_client.scan(match="user:*")
    return bool(keys)


def _get_redis_user(username):
    user_str = redis_client.get(f"user:{username}")
    if not user_str:
        return {}
    return json.loads(user_str.decode("utf-8"))


def get_user_by_id(id):
    _, keys = redis_client.scan(match="user:*")
    data = redis_client.mget(keys)
    res = None
    for d in data:
        user_dict = json.loads(d.decode("utf-8"))
        if user_dict.get("id") == id:
            res = User(
                id=user_dict.get("id"),
                username=user_dict.get("username"),
            )
    return res


def get_user(username):
    cache_user = _get_redis_user(username)
    if not cache_user:
        return
    return User(
        id=cache_user.get("id"),
        username=cache_user.get("username"),
    )


def save_user(username, password):
    user = {
        "id": str(uuid.uuid4()),
        "username": username,
        "password": get_password_hash(password),
    }
    redis_client.set(f"user:{username}", json.dumps(user))


def get_password_hash(password) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_password = hashed_password.decode("utf8")
    return string_password


def validate_login(username, password):
    cache_user = _get_redis_user(username)
    if not cache_user:
        return False
    return _verify_password(password, cache_user.get("password"))


def _verify_password(plain_password, hashed_password) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password)
