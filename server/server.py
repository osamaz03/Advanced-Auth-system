from fastapi import FastAPI,Header
from pydantic import BaseModel
import json
import bcrypt
import os
from jose import jwt,JWTError
from datetime import datetime,timedelta


app = FastAPI()

USER_FILE = "user_file.json"
SECRET_KEY = "MY-project-KEY"
ALGORIHM  = "HS256"
TOKEN_EXPIRE_MINUTES = 30


#Storage
def load_user():
    if not os.path.exists(USER_FILE):
        return{}
    
    with open(USER_FILE,"r",encoding="utf-8") as f:
        return json.load(f)
    

def save_user(users):
    with open(USER_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,indent=4)

#Security
def hash_password(password:str):
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
    return hashed.decode("utf-8")

def verify_password(password:str,hashed_password:str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_token(username:str):
    payload = {
        "sub" :username,
        "exp" : datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORIHM)


def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORIHM)
        return payload["sub"]
    except JWTError:
        return None
    

class User(BaseModel):
    username : str
    password : str


@app.post("/register")

def register(user : User):
    users = load_user()

    if user.username in users:
        return {"error" : "username already exists"}
    
    users[user.username] = hash_password(user.password)
    save_user(users)

    return {"message" : "User registered successfully"}

@app.post("/login")

def login(user : User):
    users = load_user()

    if user.username not in users:
        return {"error" : "User not found"}
    
    if not verify_password(user.password,users[user.username]):
        return {"error" : "Wrong password"}
    
    token = create_token(user.username)
    return {"token": token}


@app.get("/protected")
def protected_route(authorization: str = Header(None)):
    if not authorization:
        return {"error" : "Token missing"}
    
    username = verify_token(authorization)

    if not username:
        return {"error" : "Invalid token"}
    
    return {"message" : f"Welcome {username}"}
