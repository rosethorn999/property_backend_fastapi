from fastapi import APIRouter, Depends
from app import config
from app.routers import product, users
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2

google_oauth_client = GoogleOAuth2(
    config.settings.oauth2_google_client_id, config.settings.oauth2_google_client_secret
)
facebook_oauth_client = FacebookOAuth2(
    config.settings.oauth2_facebook_client_id,
    config.settings.oauth2_facebook_client_secret,
)
api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(product.router)
api_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
api_router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        config.settings.secret,
        redirect_url=config.settings.oauth2_google_redirect_url,
        associate_by_email=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_oauth_router(
        facebook_oauth_client,
        auth_backend,
        config.settings.secret,
        redirect_url=config.settings.oauth2_facebook_redirect_url,
        associate_by_email=True,
    ),
    prefix="/auth/facebook",
    tags=["auth"],
)


@api_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


# api_router.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
