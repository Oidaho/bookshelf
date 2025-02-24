import uvicorn
from configs import configs

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=6177,
        reload=configs.DEBUG_MODE,
    )
