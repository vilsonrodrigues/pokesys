from fastapi import APIRouter


router = APIRouter()

@router.get("/", tags=["app"])
async def root():
    return {"message": "PokeSys is running"}
