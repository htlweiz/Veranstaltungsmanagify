from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Depends, HTTPException, Response, status, APIRouter
from db.model import User
from api.model import SignupSchema, LoginSchema, LoginDB, MSALLogin
from expiringdict import ExpiringDict
from crud import users
import jwt
import bcrypt
from fastapi.responses import HTMLResponse
import msal
import os
from fastapi import HTTPException

temp_users = ExpiringDict(max_len=9999, max_age_seconds=15 * 60)

router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
SCOPES = ["User.Read"]
# Probably wrong
REDIRECT_URI = "https://localhost:8002/oauth2-redirect"

msal_client = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)


def get_info_from_token(token: str) -> tuple[str, str]:
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        email = decoded_token.get("unique_name") or decoded_token.get("upn")
        username = decoded_token.get("preferred_username") or decoded_token.get("name")
        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")
        if not username:
            raise HTTPException(status_code=400, detail="Username not found in token")

        return email, username
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")


def create_user_from_token(access_token: str) -> User:
    email, username = get_info_from_token(access_token)
    user = SignupSchema(email=email, password="", role_id=1, username=username)
    return users.create(user)


@router.post("/login/ms", status_code=200, response_model=LoginDB, tags=["auth"])
async def msal_login(token: str) -> User | None:
    result = msal_client.acquire_token_by_authorization_code(
        code=token,
        scopes=["User.Read"],
        redirect_uri="https://localhost:8002/oauth2-redirect",
    )

    if "access_token" in result:
        access_token = result["access_token"]
        email, _ = get_info_from_token(access_token)
        user = users.get_by_email(email)
        if user:
            return user
        else:
            return create_user_from_token(access_token)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    

############################### Unfinished alternative login for easier testing
# Not in working state, error on get_token ("Authentication code not found")
@router.get("/auth_flow", tags=["auth"])
async def get_auth_flow():
    auth_flow = msal_client.initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)
    return {auth_flow["auth_uri"]}

@router.post("/signup", status_code=201, response_class=HTMLResponse, tags=["auth"])
async def signup(user: SignupSchema):
    try:
        created = users.create(user)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

    response = Response(status_code=status.HTTP_201_CREATED)
    response.set_cookie(
        "access_token",
        value=f"{created.access_token}",
        httponly=True,
        secure=True,
        samesite="none",
    )
    return response


@router.post("/login", status_code=200, response_model=None, tags=["auth"])
async def login(login_user: LoginSchema, response: Response):
    user = users.get_by_email(login_user.email)
    if not user:
        return Response("User not found", status_code=404)
    if not bcrypt.checkpw(
        login_user.password.encode("utf-8"), str(user.password).encode("utf-8")
    ):
        return Response("Invalid Password", status_code=401)
    access_token = user.access_token

    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        "access_token",
        value=f"{access_token}",
        httponly=True,
        secure=True,
        samesite="none",
    )
    return response


@router.get("/oauth2-redirect", status_code=200)
async def msal_response(request: Request, response: Response):
    access_token = (await msal_login(request.query_params.get("code"))).access_token
    return RedirectResponse(
        url="https://localhost:5173/login?access_token=" + access_token
    )
