from fastapi import APIRouter


router = APIRouter()

@router.get("/health", tags=["app"])
async def health():
    return {"status": "ok"}
