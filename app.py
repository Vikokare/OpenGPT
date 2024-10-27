import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

import auth
from llm_manager import llm_response


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Summarize Books",
            message="Help me summarize a refrence book",
            icon="./public/scholar_icon.png",
        ),

        cl.Starter(
            label="Data Scientist",
            message="Research topic ___",
            icon="./public/idea_icon.png",
        ),

        cl.Starter(
            label="Crawler",
            message="Crawl for ___",
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
                    "mixtral-8x7b-32768", 
                    "llama3-8b-8192",
                    "llama3-70b-8192", 
                ],
                initial_index=0,
            ),
            Switch(
                id="Streaming", 
                label="Streaming", 
                initial=False
            )
        ]
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    # settings = await cl.get_settings()
    # model = settings["Model"]
    # temperature = settings["Streaming"]
    response = llm_response(message)
    
    await cl.Message(
        content=response
    ).send()


@cl.on_settings_update
async def settings_update(settings):
    print("settings Updated;;")


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