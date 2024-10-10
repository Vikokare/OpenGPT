import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

import auth
import document_handler
import llm_manager


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
    print(app_user)
    if not app_user:
        await cl.redirect("/auth")
    else:
        # await cl.Message(f"Hello {app_user.identifier}").send()
        print("----")

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Model",
                values=[
                    "mixtral-8x7b-32768", 
                    "llama3-70b-8192", 
                    "llama3-8b-8192"
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
    ...


@cl.on_settings_update
async def settings_update(settings):
    print(settings)
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


# @cl.on_file_upload
# async def handle_file_upload(file):
#     cl.info(f"File upload: {file.name}")
#     loader = PyPDFLoader(file_path=file.path)  # Assuming file is stored temporarily
#     pages = loader.load_and_split()
#     await cl.Message(content=f"Processed {len(pages)} pages from {file.name}.").send()


# if message.content == "Help me summarize a refrence book":
        
#         # Wait for the user to upload a file
#         while files == None:
#             files = await cl.AskFileMessage(
#                 content="Please upload a text file to begin!",
#                 accept=["text/plain", "application/pdf"],
#                 max_size_mb=20,
#                 timeout=180,
#             ).send()

#         file = files[0]

#         msg = cl.Message(content=f"Processing `{file.name}`...")
#         await msg.send()

#         # await cl.Message(
#         #     content=f"{files[0].name} is successfully uploaded"
#         # ).send()
        
#         # loader = PyPDFLoader(files[0].path)
#         # pages = loader.load_and_split()
        
#         # return
        
    
#     elif message.content == "Crawl for ___":
#         ...


#     # similar_docs = get_similar_doc(message.content, k=1)
    
#     # await cl.Message(
#     #     content=similar_docs
#     # ).send()