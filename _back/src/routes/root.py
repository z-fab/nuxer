from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/hello")
async def hello():
    return {"message": "Hello, FabBank!"}
