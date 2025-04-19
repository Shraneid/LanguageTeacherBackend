import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI

from constants import model_id

llm = ChatGoogleGenerativeAI(model=model_id, google_api_key="AIzaSyBo9whw03Cw6CS1Ps8dGYYAZuR35Q57kjA")

@cl.on_chat_start
async def main():
    await cl.Message(content="Hello3! Ask me anything powered by Gemini 2.0 Flash via Langchain.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    response = llm.invoke(message.content)

    await cl.Message(content=response.content).send()