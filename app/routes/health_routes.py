from fastapi import APIRouter
from app.utils.health import check_database, check_external_service
import time
router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    start_time = time.time()
    
    db_status = await check_database()
    api_status = await check_external_service()

    total_time_taken = time.time() - start_time

    return {
        "status": "Healthy" if db_status["status"] == "Healthy" and api_status["status"] == "Healthy" else "Unhealthy",
        "totalTimeTaken": f"{total_time_taken:.6f}",
        "entities": [db_status, api_status]
    }