import logging
from typing import Optional, Annotated

import firebase_admin
from fastapi import FastAPI, Request, Response, Header, Body, Depends, HTTPException
from firebase_admin.exceptions import FirebaseError
from starlette.middleware.cors import CORSMiddleware
from chainlit.utils import mount_chainlit
from firebase_admin import auth, credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        logging.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        logging.info(f"Error initializing Firebase Admin SDK: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.info(f"Headers: {request.headers}")

    response = await call_next(request)
    return response

async def verify_firebase_token(
    token: Annotated[str, Header(alias="Authorization")]
):
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    try:
        decoded_token = auth.verify_id_token(token.split("Bearer ")[1])
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return decoded_token
    except FirebaseError as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication token: {e}")

@app.get("/")
def read_main(request: Request, decoded_token: str = Depends(verify_firebase_token)):
    logging.info("decoded_token")
    logging.info(decoded_token)

    user_id = decoded_token.get('user_id')

    return {"message": "This is working from main app"}

mount_chainlit(app=app, target="src/chainlit_app.py", path="/chainlit")
