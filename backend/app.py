import asyncio
import chainlit as cl
from chainlit.input_widget import Select, Switch, TextInput

from manager import LLMService
import auth

class SettingsManager:
    def __init__(self):
        self.settings = {
            "Model": "llama3-8b-8192",
            "Streaming": True,
            "GROQ_API_KEY": None,
        }

    def update(self, new_settings):
        self.settings.update(new_settings)
        if self.settings["GROQ_API_KEY"]:
            cl.user_session.set("GROQ_API_KEY", self.settings["GROQ_API_KEY"])

    def get(self, key):
        return self.settings.get(key)

    def get_all(self):
        return self.settings


class LLMCalls:
    async def generate(self, prompt, model):
        return await LLMService.generate(prompt, model)

    async def stream_response(self, text: str):
        tokens = text.split(" ")
        msg = cl.Message(content="")
        await msg.send()
        for token in tokens:
            await msg.stream_token(token + " ")
            await asyncio.sleep(0.1)
        await msg.send()


class ChatHandler:
    def __init__(self, settings_manager, llm_service):
        self.settings = settings_manager
        self.llm = llm_service

    async def handle_start(self):
        app_user = cl.user_session.get("user")
        if not app_user:
            await cl.redirect("/auth")

        await cl.ChatSettings(
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
                Switch(id="Streaming", label="Streaming", initial=True),
                TextInput(id="GROQ_API_KEY", label="GROQ API KEY", initial=""),
            ]
        ).send()

    async def handle_message(self, message: cl.Message):
        model = self.settings.get("Model")
        response = await self.llm.generate(message.content, model)
        await self.llm.stream_response(response)

    async def handle_stop(self):
        await cl.Message(content="Chat Interrupted!").send()

    async def handle_end(self):
        await cl.Message(content="Thank You!").send()


@cl.set_starters
async def starters():
    icon_url = "https://cdn-icons-png.flaticon.com/512/888/888879.png"
    return [
        cl.Starter("Healthy Eating Tips", "What are some tips for maintaining a healthy diet?", icon_url),
        cl.Starter("Travel Destinations", "Can you suggest some amazing travel destinations?", icon_url),
        cl.Starter("Space Exploration", "Tell me about the latest discoveries in space exploration.", icon_url),
        cl.Starter("Personal Finance Advice", "How can I manage my finances better?", icon_url),
        cl.Starter("Tech Innovations", "What are the latest tech innovations?", icon_url),
        cl.Starter("Motivational Quotes", "Share some motivational quotes to boost my mood.", icon_url),
        cl.Starter("Fitness Workouts", "What are some effective fitness workouts?", icon_url),
        cl.Starter("Mental Health Tips", "How can I improve my mental health?", icon_url),
        cl.Starter("Career Advice", "How do I advance in my career?", icon_url),
        cl.Starter("Art & Creativity", "Can you give me tips to enhance my creativity?", icon_url),
    ]


settings_manager = SettingsManager()
llm_service = LLMService()
chat_handler = ChatHandler(settings_manager, llm_service)


@cl.on_chat_start
async def on_chat_start():
    await chat_handler.handle_start()

@cl.on_message
async def on_message(message: cl.Message):
    await chat_handler.handle_message(message)

@cl.on_settings_update
async def on_settings_update(new_settings):
    settings_manager.update(new_settings)

@cl.on_stop
async def on_stop():
    await chat_handler.handle_stop()

@cl.on_chat_end
async def on_chat_end():
    await chat_handler.handle_end()


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)