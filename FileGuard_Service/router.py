from fastapi import APIRouter, Depends
import os

from FileGuard_Service.dependency import validated_pdf
from FileGuard_Service.detect_file import detect_files

router = APIRouter()

from fastapi import HTTPException

@router.post("/detect")
def scan_pdf(file_path: str = Depends(validated_pdf)):
    try:
        result = detect_files(file_path)
        return result
    except Exception as e:
        print("Detection error:", e)
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)