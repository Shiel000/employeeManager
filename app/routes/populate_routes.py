from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.seed import populate_dummy_data
from app.models.base import get_db

router = APIRouter()

@router.post("/seed-data")
async def seed_database(db: AsyncSession = Depends(get_db)):
    try:
        await populate_dummy_data(db)
        return {"status": "success", "message": "Dummy data populated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding data: {str(e)}")
