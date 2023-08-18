from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.user_router import user_router
from app.controllers.auth_router import auth_router


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
        CORSMiddleware, 
        allow_origins=['*'],
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"]
    )