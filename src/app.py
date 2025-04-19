from http.client import HTTPException

import firebase_admin
from fastapi import FastAPI, Header
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from chainlit.utils import mount_chainlit
from firebase_admin import auth, credentials

if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")

app = FastAPI(middleware=[
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust as needed for security in production
        allow_methods=["*"],
        allow_headers=["*"],
    )
])

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        id_token = authorization.split("Bearer ")[1]
        decoded_token = await auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return uid
    except firebase_admin.exceptions.FirebaseError as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication token: {e}")

@app.get("/")
def read_main():
    return {"message": "This is working from main app"}

# if True:
mount_chainlit(app=app, target="src/my_cl_app.py", path="/chainlit")
# else:
#     mount_chainlit(app=app, target="my_cl_app.py", path="/chainlit")

@app.get("/health")
async def health():
    return {"status": "ok"}