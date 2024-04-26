from datetime import datetime
import uuid
from typing import Any, Dict, Optional, Union
from fastapi import Depends, Request, Response
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    UUIDIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models import User
from app.database import get_user_db
from app.schemas import UserCreate
from app import config
from string import Template
import smtplib
from fastapi import BackgroundTasks
import email.message

SECRET = config.settings.secret


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __init__(
        self, user_db: SQLAlchemyUserDatabase, background_tasks: BackgroundTasks
    ):
        super().__init__(user_db)
        self.background_tasks = background_tasks

    async def send_email(self, sender, recipient, subject, body):
        msg = email.message.Message()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(body)

        mail = smtplib.SMTP(config.settings.smtp_host, config.settings.smtp_port)
        if config.settings.smtp_use_tls:
            mail.starttls()
        mail.login(config.settings.smtp_host_user, config.settings.smtp_host_password)
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()

    async def __send_verify_mail(self, user: User, token: str):
        emailTemplate = Template(
            '<div><img class="image-placeholder" src="https://i.imgur.com/TisDgEE.gif" style="height:500px;width:300px" alt="gif-wheeee-animated-photo-of-cat-on-bench-I-have-no-regrets"><h1>Hi, welcome to to Property!</h1><br><p>Please click link to finish your registration. <a href="$linkAddr">$linkAddr</a></p><p>Thank you for using <a href="$frontendHost">Property</a>.</p></div>'
        )
        subject = "Thank you for using Property"
        frontendHost = config.settings.frontend_host
        linkAddr = f"{frontendHost}/en/verify?token={token}"
        body = emailTemplate.substitute(frontendHost=frontendHost, linkAddr=linkAddr)
        print(f"@@@@@ mail triggered: {linkAddr}")
        recipient = user.email
        sender = config.settings.smtp_host_user
        self.background_tasks.add_task(
            self.send_email, sender, recipient, subject, body
        )

    async def __send_forget_password_mail(self, user: User, token: str):
        emailTemplate = Template(
            '<img class="image-placeholder" src="https://i.imgur.com/kuqN4bl.jpeg" style="height:876px;width:300px" alt="Front-page-Password"><h1>Hi, welcome to to Property!</h1><br><p>Please click link to reset your password. <a href="$linkAddr">$linkAddr</a></p><p>Thank you for using <a href="$frontendHost">Property</a>.</p></div>'
        )
        subject = "Password Reset"
        frontendHost = config.settings.frontend_host
        linkAddr = f"{frontendHost}/en/reset-password?token={token}"
        body = emailTemplate.substitute(frontendHost=frontendHost, linkAddr=linkAddr)
        print(f"@@@@@ mail triggered: {linkAddr}")
        recipient = user.email
        sender = config.settings.smtp_host_user
        self.background_tasks.add_task(
            self.send_email, sender, recipient, subject, body
        )

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        await self.request_verify(user)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # send an e-mail with the link (and the token) that allows the user to verify their e-mail.
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        await self.__send_verify_mail(user, token)

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        await self.user_db.update(user, {"last_login": datetime.now()})
        print(f"User {user.id} logged in.")

    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has been verified")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        await self.__send_forget_password_mail(user, token)

    async def on_before_delete(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} is going to be deleted")

    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} is successfully deleted")


# async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
#     yield UserManager(user_db)
async def get_user_manager(
    background_tasks: BackgroundTasks,
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db, background_tasks)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
