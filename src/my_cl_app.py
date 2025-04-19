import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from constants import model_id

gemini_api_key = os.environ.get("GEMINI_API_KEY")
llm = None
if gemini_api_key:
    llm = ChatGoogleGenerativeAI(model=model_id, google_api_key=gemini_api_key)
else:
    print("Warning: GEMINI_API_KEY not found. LLM features will be unavailable.")

@cl.on_chat_start
async def main():
    await cl.Message(content="Hello! Ask me anything powered by Gemini 2.0 Flash via Langchain.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    if llm:
        response = llm.invoke(message.content)
        await cl.Message(content=response.content).send()
    else:
        await cl.Message(content="LLM not initialized due to missing API key.").send()