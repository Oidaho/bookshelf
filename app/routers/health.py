from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import platform
import socket
import datetime

router = APIRouter()


@router.get(path="/health", summary="Health Check", tags=["Health"])
async def health_check():
    try:
        health_status = {
            "status": "healthy",
            "system": {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        return JSONResponse(content=health_status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
