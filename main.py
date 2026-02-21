from fastapi import FastAPI
from FileGuard_Service.router import router as fileguard_router

app = FastAPI(title="Guardify API")

app.include_router(fileguard_router, prefix="/fileguard", tags=["FileGuard"])