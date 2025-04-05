from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware import Middleware
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.db import async_engine
from src.core.settings import settings
from src.web.api import api_router
from src.web.api.signing import signing

EXCLUDED_PATHS = {"/docs", "/redoc", "/openapi.json", "/metrics"}


class SignatureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        try:
            await signing(request)
        except HTTPException as error:
            return ORJSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail},
            )
        response = await call_next(request)
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    prometheus_inst.expose(app)
    yield
    # Cleanup idle connections
    await async_engine.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    middleware=[Middleware(SignatureMiddleware)],
)

app.include_router(api_router, prefix="/api")

prometheus_inst = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics"],
)

prometheus_inst.instrument(
    app, metric_namespace=settings.namespace, metric_subsystem=settings.name
)
