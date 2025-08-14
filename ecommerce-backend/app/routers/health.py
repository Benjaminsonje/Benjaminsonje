from fastapi import APIRouter

router = APIRouter()


@router.get("/liveness")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readiness")
async def readiness() -> dict[str, str]:
    # In future, check DB connectivity, external services, etc.
    return {"status": "ready"}