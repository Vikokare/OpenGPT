import chainlit as cl
from typing import Optional

# Simulated user storage (replace with a database in a real application)
users_db = {
    "vaibhav": {"password": "222", "role": "ADMIN"},
    "Nikita": {"password": "111", "role": "USER"}
}

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    # print("USERNAME", username, "PASSWORD", password)
    user = users_db.get(username)
    if user and user["password"] == password:
        return cl.User(
            identifier=username, 
            metadata={"role": user["role"]}
        )
    return None


@cl.on_logout
async def on_logout():
    cl.user_session.clear()
    await cl.redirect("/auth")