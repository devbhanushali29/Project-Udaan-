from fastapi import APIRouter, HTTPException
from service import translate_text

router = APIRouter()

# Translation route
@router.get("/translate/get")
def translate_get(text: str, target_lang: str):
    """
    Translate a single text to the target language
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text parameter is required")
    if not target_lang:
        raise HTTPException(status_code=400, detail="Target language parameter is required")

    try:
        translated = translate_text(text, target_lang)
        return {
            "original": text,
            "translated": translated,
            "language": target_lang
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check route
@router.get("/health")
def health():
    """
    Health check endpoint to confirm API is running
    """
    return {"status": "ok", "message": "Udaan Translation API is running"}
