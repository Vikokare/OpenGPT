import re
import os
import chainlit as cl
from typing import Optional, Dict

GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET")

# Simulated user storage (replace with a database in a real application)
users_db = {
    "vaibhav@gmail.com": {"password": "0000", "role": "ADMIN"},
    "Nikita@gmail.com": {"password": "1111", "role": "USER"}
}

def validate_email(user_email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, user_email):
        return True
    return False

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    if not validate_email(username): return None
    user = users_db.get(username)
    if user and user["password"] == password:
        return cl.User(
            identifier=username, 
            metadata={"role": user["role"]}
        )
    return None


@cl.on_logout
async def on_logout():
    cl.user_session.user = None
    # await cl.redirect("/auth")


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    if provider_id == "google":
        return cl.User(
            identifier=raw_user_data["email"],
            metadata={"role": "USER"}
        )
    return default_user