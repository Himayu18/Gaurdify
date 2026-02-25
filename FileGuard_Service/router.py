from fastapi import APIRouter, Depends
import os

from FileGuard_Service.dependency import validated_pdf
from FileGuard_Service.detect_file import detect_files

router = APIRouter()

from fastapi import HTTPException

@router.post("/detect")
def scan_pdf(file_path: str = Depends(validated_pdf)):
    try:
        print(f"Processing file: {file_path}")
        result = detect_files(file_path)
        print("Prediction success:", result)
        return result

    except Exception as e:
        print("===== ERROR START =====")
        print(f"File: {file_path}")
        print("Error:", str(e))
        print("===== ERROR END =====")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)