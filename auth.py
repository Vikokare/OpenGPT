import re
import os
import chainlit as cl
from typing import Optional, Dict

GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET")

class UserStore:
    """Handles user data storage and validation"""
    def __init__(self):
        self.users_db = {
            "vaibhav@gmail.com": {"password": "0000", "role": "ADMIN"},
            "Nikita@gmail.com": {"password": "1111", "role": "USER"}
        }

    def get_user(self, email: str):
        return self.users_db.get(email.lower())
    
    def validate_password(self, email: str, password: str) -> bool:
        user = self.get_user(email)
        return user and user["password"] == password
    
    def get_role(self, email: str) -> str:
        user = self.get_user(email)
        return user["role"]

class Auth:
    """Handles authentication of user and google auth service"""
    def __init__(self, user_store: UserStore):
        self.user_store = user_store
        self.EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate_email(self, email: str) -> bool:
        return re.match(self.EMAIL_REGEX, email) is not None

    def authenticate(self, email: str, password: str) -> Optional[cl.User]:
        email = email.lower()
        if self.validate_email(email) and self.user_store.validate_password(email, password):
            return cl.User(
                identifier=email,
                metadata={"role": self.user_store.get_role(email)}
            )
        return None

    def handle_oauth(self, provider_id: str, raw_user_data: Dict[str, str]) -> cl.User:
        email = raw_user_data["email"].lower()
        role = self.user_store.get_role(email)
        return cl.User(identifier=email, metadata={"role": role})


user_store = UserStore()
auth_service = Auth(user_store)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    return auth_service.authenticate(username, password)


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User
) -> Optional[cl.User]:
    if provider_id == "google":
        return auth_service.handle_oauth(provider_id, raw_user_data)
    return default_user


@cl.on_logout
async def on_logout():
    cl.user_session.user = None