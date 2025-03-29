from fastapi import APIRouter
from sqlmodel import select

from src.web.deps import SessionDep

router = APIRouter()


@router.get("/")
def hello(name: str = "World"):
    return f"Hello, {name}!"


@router.get("/healthz")
async def health_check(session: SessionDep):
    """Healthcheck API Operation."""
    result = (await session.execute(select(1))).first()

    if result is None:
        return {
            "status": "error",
            "message": "No health status found",
        }

    return {"status": "ok"}
