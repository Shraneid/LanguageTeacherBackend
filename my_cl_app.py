import chainlit as cl
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from constants import model_id

# Load environment variables
load_dotenv()

@cl.on_chat_start
async def main():
    """Initialize the conversation chain for this session."""
    llm = ChatGoogleGenerativeAI(model=model_id)
    llm.invoke("Write me a ballad about LangChain")
    
    # Add memory to the conversation chain
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # Store in user session
    cl.user_session.set("conversation", conversation)
    
    # Send welcome message
    await cl.Message(
        content="Welcome to the Language Teacher! How can I help you today?",
        author="Language Teacher"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):  # Explicitly type the message parameter
    """Process incoming messages using the conversation chain."""
    # Get conversation from user session
    conversation = cl.user_session.get("conversation")
    
    if not conversation:
        await cl.Message(
            content="Error: Conversation not initialized.",
            author="System"
        ).send()
        return
    
    # Show thinking indicator
    with cl.Step("Thinking..."):
        try:
            # Get response using LangChain
            response = conversation.predict(input=message.content)
            
            # Send response back to user
            await cl.Message(
                content=response,
                author="Language Teacher"
            ).send()
            
        except Exception as e:
            # Handle errors
            error_message = f"An error occurred: {str(e)}"
            await cl.Message(
                content=error_message,
                author="System"
            ).send()
