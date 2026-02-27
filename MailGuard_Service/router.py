from fastapi import APIRouter, HTTPException, Body
from MailGuard_Service.mails import emails
from email.parser import BytesParser
from email import policy
import os
import uuid

router = APIRouter()


@router.post("/detect")
def scan_email(raw_email: str = Body(..., media_type="text/plain")):

    if not raw_email or not raw_email.strip():
        raise HTTPException(status_code=400, detail="Empty email content.")


    base_dir = os.path.dirname(__file__)
    upload_dir = os.path.join(base_dir, "emails")

    try:
        os.makedirs(upload_dir, exist_ok=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create temp directory: {str(e)}"
        )

    email_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}.eml")

    try:
        with open(email_path, "wb") as f:
            f.write(raw_email.encode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to write email content: {str(e)}"
        )

    try:
        with open(email_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        if not msg.get("From") or not msg.get("Date"):
            raise HTTPException(
                status_code=400,
                detail="Invalid MIME format."
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid MIME message: {str(e)}"
        )

    try:
        email_obj = emails(email_path)
        result = email_obj.detect_email()
        return {"result": result}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Email processing failed: {str(e)}"
        )

    finally:
        if os.path.exists(email_path):
            try:
                os.remove(email_path)
            except Exception:
                pass