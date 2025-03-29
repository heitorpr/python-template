from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.web.api import api_router
from src.web.api.signing import signing


class SignatureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        await signing(request)
        response = await call_next(request)
        return response


app = FastAPI(default_response_class=ORJSONResponse, middleware=[Middleware(SignatureMiddleware)])

app.include_router(api_router, prefix="/api")
