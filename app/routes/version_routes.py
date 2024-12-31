from fastapi import APIRouter

router = APIRouter()

@router.get("/version")
async def get_version():
    """Endpoint para obtener la versión de la aplicación."""
    return {
        "version": "1.0.0",
        "description": "Employee Manager API",
        "release_date": "2024-12-30"
    }
