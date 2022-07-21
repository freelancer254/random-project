from . import schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db, user_key: str):
    return db.get(user_key)

def get_user_by_username(db, username: str):
    return db.fetch({"email?contains": "@","username": username.lower()}).items

def get_user_by_email(db, email: str):
    return db.fetch({"email": email.lower()}).items

async def create_user(db, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user: dict = { 
    "username": user.username.lower(),
    "email": user.email.lower(),
    "hashed_password": hashed_password,
    "is_active": True #Turn to False If User has to verify email first
    }
    db.put(db_user)
    return {"data": "Your Account Has Been Successfully Created!"}

    ''' if there is need to send email and activate the user
    #send verification email
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return await mailer.simple_send(access_token, [user.email])
    

def activate_user(db, username: str):
    user = db.fetch({"username":username}).items[0]
    db.update({"is_active": True}, user["key"])
    return user
'''

def get_latest_draws(db):
    return db.fetch({"description?contains": "Random"}).items

#return all the draws for a particular user
def get_user_draws(db, username: str):
    fetched_draws =  db.fetch({"description?contains": "Random","username": username.lower()})
    all_draws = fetched_draws.items
    while fetched_draws.last:
        fetched_draws =  db.fetch({"description?contains": "Random","username": username.lower()}, last=fetched_draws.last)
        all_draws += fetched_draws.items
    return all_draws


def get_draw(db, key: str ):
    return db.get(key)


def create_user_draw(db, draw: dict):
    db_draw = db.put(draw)
    return db_draw
