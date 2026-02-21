from fastapi import UploadFile, File, HTTPException
import os
import uuid
import shutil

from FileGuard_Service.file_validator import validate_pdf  

def validated_pdf(file: UploadFile = File(...)) -> str:
    base_dir = os.path.dirname(__file__) 
    upload_dir = os.path.join(base_dir, "tmp_uploads")

    os.makedirs(upload_dir, exist_ok=True)

    tmp_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}.pdf")

    with open(tmp_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    if not validate_pdf(tmp_path):
        os.remove(tmp_path)
        raise HTTPException(status_code=400, detail="Invalid file")

    return tmp_path