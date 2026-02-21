from fastapi import FastAPI
from FileGuard_Service.router import router as fileguard_router
from MailGuard_Service.router import router as mailgaurd_router

app = FastAPI(title="Guardify API")

app.include_router(fileguard_router, prefix="/fileguard", tags=["FileGuard"])
app.include_router(mailgaurd_router,prefix="/mailguard",tags=["MailGaurd"])