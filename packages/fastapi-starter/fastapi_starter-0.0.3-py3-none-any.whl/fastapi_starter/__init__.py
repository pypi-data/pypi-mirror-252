"""The extensible FastAPI application."""

from os import getenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import NoResultFound

from .routers import auth, organisations, users

app = FastAPI(
    debug=getenv("DEBUG") == "True",
    title=getenv("APPLICATION_NAME"),
    description=getenv("APPLICATION_DESCRIPTION"),
)
"""The API application."""


app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv("FRONTEND_URL")],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router)
app.include_router(organisations.router)
app.include_router(users.router)


@app.get("/")
def index():
    """Ping application."""
    return {"Hello": "World"}


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    """Handle AuthJWTException exceptions."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(NoResultFound)
def sqlalchemy_no_result_found_exception_handler(*_):
    """Handle SQLAlchemy `NoResultFound` exceptions."""
    return JSONResponse(status_code=404, content={"detail": "Not Found"})
