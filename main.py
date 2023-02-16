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

JWT_SECRET = "39815d123dd3ef24"
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
    
class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

app = FastAPI()

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False, dependencies=[Depends(JWTBearer())])
def redoc_html(request: Request)-> HTMLResponse:
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + "/openapi.json"
    return get_redoc_html(openapi_url=openapi_url, title="API Docs")