import httpx
from asyncpg import connect, Connection, exceptions
import os
import time
from functools import wraps

async def check_database() -> dict:
    """Check database connection status."""
    start_time = time.time()
    try:
        connection: Connection = await connect(
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            database=os.getenv("POSTGRES_DB", "employeedb"),
            host="employee-manager-db"
        )
        await connection.close()
        return {
            "alias": "postgres db",
            "status": "Healthy",
            "timeTaken": f"{time.time() - start_time:.6f}",
        }
    except exceptions.PostgresError as e:
        return {
            "alias": "postgres db",
            "status": "Unhealthy",
            "timeTaken": f"{time.time() - start_time:.6f}",
            "error": str(e)
        }
    except Exception as e:
        return {
            "alias": "postgres db",
            "status": "Unhealthy",
            "timeTaken": f"{time.time() - start_time:.6f}",
            "error": str(e)
        }


async def check_external_service() -> dict:
    """Check external API availability."""
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get('https://jsonplaceholder.typicode.com/posts')
            return {
                "alias": "external service",
                "status": "Healthy" if response.status_code == 200 else "Unhealthy",
                "timeTaken": f"{time.time() - start_time:.6f}",
            }
    except httpx.RequestError as e:
        return {
            "alias": "external service",
            "status": "Unhealthy",
            "timeTaken": f"{time.time() - start_time:.6f}",
            "error": str(e)
        }
    except Exception as e:
        return {
            "alias": "external service",
            "status": "Unhealthy",
            "timeTaken": f"{time.time() - start_time:.6f}",
            "error": str(e)
        }
        

