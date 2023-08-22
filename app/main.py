from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from uvicorn import run

from .controllers.auth import auth_router
from .controllers.user import user_router
from .configuration import Settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


# @app.middleware("http")
# async def add_csp_header(request: Request, call_next):
#     response = await call_next(request)
#     csp_value = "default-src 'self'; img-src 'self' data; script-src 'self';"

#     response.headers["Content-Security-Policy"] = csp_value

#     return response 


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"root": "route"}


if __name__ == "__main__":
    run(app, port=10000)
