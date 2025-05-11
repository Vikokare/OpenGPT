import asyncio
import chainlit as cl
from chainlit.input_widget import Select, Switch, TextInput

import auth
from llm_manager import llm_response

settings = {
    "Model": "llama3-8b-8192",
    "Streaming": True,
    "GROQ_API_KEY": None,
}

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Exam preprations",
            message="How to prepare for Exams?",
            icon="./public/scholar_icon.png",
        ),

        cl.Starter(
            label="Brillance Mind Ratan Tata",
            message="Give some inspiritional story about Sir Ratan Tata",
            icon="./public/idea_icon.png",
        ),

        cl.Starter(
            label="Dragons Tale",
            message="Are dragons real?",
            icon="./public/icons8-flame-64.png",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user")
    if not app_user:
        await cl.redirect("/auth")

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Model",
                values=[
                    "llama3-8b-8192",
                    "llama3-70b-8192", 
                    "mixtral-8x7b-32768", 
                ],
                initial_index=0,
            ),
            Switch(
                id="Streaming", 
                label="Streaming", 
                initial=True
            ),
            TextInput(
                id="GROQ_API_KEY", 
                label="GROQ API KEY", 
                initial=""
            ),
        ]
    ).send()

@cl.on_message
async def on_message(message: cl.Message):

    response = await llm_response(message.content, settings["Model"])

    response = response.split(" ")
    
    msg = cl.Message(content="")
    await msg.send()
    for token in response:
        await msg.stream_token(token + " ")
        await asyncio.sleep(0.1) 
    await msg.send()


@cl.on_settings_update
async def on_settings_update(new_settings):
    global settings
    settings.update(new_settings)
    if settings["GROQ_API_KEY"]:
        cl.user_session.set("GROQ_API_KEY", settings["GROQ_API_KEY"])
    # print("Settings Updated", settings)


@cl.on_stop
async def on_stop():
    await cl.Message(
        content="Chat Interrupted!"
    ).send()
    


@cl.on_chat_end
async def on_chat_end():
    await cl.Message(
        content="Thank You!"
    ).send()


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)