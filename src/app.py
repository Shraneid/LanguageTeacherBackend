import firebase_admin
from fastapi import FastAPI
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

@app.get("/")
def read_main():
    return {"message": "This is working from main app"}

mount_chainlit(app=app, target="my_cl_app.py", path="/chainlit")

@app.get("/health")
async def health():
    return {"status": "ok"}