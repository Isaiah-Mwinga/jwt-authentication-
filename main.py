import time
from dataclasses import dataclass

import jwt
from fastapi import FastAPI, Request, Body, Depends, HTTPException
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
