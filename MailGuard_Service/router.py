from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import shutil

from MailGuard_Service.mails import emails  

router = APIRouter()

@router.post("/detect")
def scan_email(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".eml"):
        raise HTTPException(status_code=400, detail="Only .eml files allowed")

    base_dir = os.path.dirname(__file__)
    upload_dir = os.path.join(base_dir, "emails")
    os.makedirs(upload_dir, exist_ok=True)


    emails_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}.eml")

    with open(emails_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    try:
        email_obj = emails(emails_path)
        result = email_obj.detect_email()
        return result
    finally:
        if os.path.exists(emails_path):
            os.remove(emails_path)