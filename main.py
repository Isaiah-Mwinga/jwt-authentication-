import time
from dataclasses import dataclass

import jwt
from fastapi import FastAPI, Request, Body, Depends, HTTPException
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

@dataclass
class User:
    email: EmailStr
    password: str

users = [
    User(
        email="john@doe",
        password="secret",
    )
]

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

def authenticate(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False    

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {"access_token": token}

def sign_jwt(user_id: str)-> dict(str, str):
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >= time.time() else None 
    except:
            return {}   
    