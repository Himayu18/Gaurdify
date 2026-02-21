from fastapi import APIRouter, Depends
import os

from FileGuard_Service.dependency import validated_pdf
from FileGuard_Service.detect_file import detect_files

router = APIRouter()

@router.post("/detect")
def scan_pdf(file_path: str = Depends(validated_pdf)):
    try:
        result = detect_files(file_path)
        return result
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)