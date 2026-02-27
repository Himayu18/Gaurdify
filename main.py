import os
from fastapi import FastAPI
from FileGuard_Service.router import router as fileguard_router
from MailGuard_Service.router import router as mailgaurd_router
from TextGaurd_Service.router import router as textgaurd_router

app = FastAPI(title="Guardify API")

@app.get("/health")
async def health_check():
    api_key_loaded = bool(os.getenv("OPENROUTER_API_KEY"))
    return {"status": "healthy","ai_configured": api_key_loaded}

app.include_router(fileguard_router, prefix="/fileguard", tags=["FileGuard"])
app.include_router(mailgaurd_router,prefix="/mailguard",tags=["MailGaurd"])
app.include_router(textgaurd_router,prefix="/textguard",tags=["TextGaurd"])