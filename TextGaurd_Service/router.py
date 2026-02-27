from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from TextGaurd_Service.text_classifier import evaluate_message

router = APIRouter()

class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)


@router.post("/detect")
async def scan_message(payload: MessageRequest):
    try:
        message = payload.message.strip()

        if not message:
            raise HTTPException(status_code=400,detail="Message cannot be empty or whitespace.")

        result = evaluate_message(message)
        if not isinstance(result, dict):
            raise HTTPException(status_code=502,detail="Unexpected response format from AI service.")

        if result.get("error"):
            raise HTTPException(status_code=502,detail="AI service failed to evaluate the message. Please try again later.")
        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500,detail="Message evaluation service is currently unavailable.")