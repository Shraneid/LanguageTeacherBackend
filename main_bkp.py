from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_vertexai import ChatVertexAI
from chainlit.utils import mount_chainlit
from constants import model_id

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Language Teacher API",
              description="A FastAPI application with Chainlit integration")


# Initialize models with Config settings for arbitrary types
class ConversationRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class ConversationResponse(BaseModel):
    response: str
    conversation_id: str

    class Config:
        arbitrary_types_allowed = True


# Store conversation chains for API requests
conversation_chains = {}


# FastAPI endpoint for direct API access
@app.post("/api/conversation", response_model=ConversationResponse)
async def get_conversation(request: ConversationRequest):
    # Check if Google credentials are available
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise HTTPException(status_code=500, detail="Google credentials not configured")

    # Get or create conversation chain
    if request.conversation_id and request.conversation_id in conversation_chains:
        conversation = conversation_chains[request.conversation_id]
    else:
        # Create a new conversation chain with Vertex AI
        llm = ChatVertexAI(
            model_name=model_id,  # Match model used in my_cl_app.py
            temperature=0.7,
            max_output_tokens=1024,
        )
        memory = ConversationBufferMemory()
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True
        )
        # Generate a simple ID if not provided
        conversation_id = request.conversation_id or f"conv_{len(conversation_chains) + 1}"
        conversation_chains[conversation_id] = conversation

    # Get response
    response = conversation.predict(input=request.query)

    return ConversationResponse(
        response=response,
        conversation_id=request.conversation_id or f"conv_{len(conversation_chains)}"
    )


@app.get("/api")
def read_main():
    return {"message": "Welcome to Language Teacher API. Use /api/conversation endpoint for programmatic access."}


# Mount the Chainlit app at the root path
mount_chainlit(app=app, path="/", target="my_cl_app.py")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
