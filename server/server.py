from fastapi import FastAPI
from pydantic import BaseModel
import json
import bcrypt
import os

app = FastAPI()

USER_FILE = "user_file.json"

def load_user():
    if not os.path.exists(USER_FILE):
        return{}
    
    with open(USER_FILE,"r",encoding="utf-8") as f:
        return json.load(f)
    

def save_user(users):
    with open(USER_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,indent=4)


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


class User(BaseModel):
    username : str
    password : str


@app.post("/register")

def register(user : User):
    users = load_user()

    if user.username in users:
        return {"error" : "username alredy exists"}
    
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
    
    return {"message" : "login successful"}
