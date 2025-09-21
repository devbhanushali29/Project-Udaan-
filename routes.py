from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from service import translate_text, translate_bulk, translation_logs
from model import TranslateRequest, VALID_LANG_CODES

router = APIRouter()

# POST endpoint for bulk translation
@router.post("/translate")
def translate_post(request: TranslateRequest):
    # Input validation
    if request.target_lang not in VALID_LANG_CODES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid target language code. Choose from {VALID_LANG_CODES}"
        )
    if not request.texts or any(not t.strip() for t in request.texts):
        raise HTTPException(status_code=400, detail="Texts cannot be empty")
    if any(len(t) > 1000 for t in request.texts):
        raise HTTPException(status_code=400, detail="Each text must be <= 1000 characters")

    translations = translate_bulk(request.texts, request.target_lang)
    response = [
        {"original": t, "translated": tr, "language": request.target_lang}
        for t, tr in zip(request.texts, translations)
    ]
    return JSONResponse(content=response, media_type="application/json; charset=utf-8")


# GET endpoint for single translation
@router.get("/translate/get")
def translate_get(
    text: str = Query(..., max_length=1000),
    target_lang: str = Query(...)
):
    if target_lang not in VALID_LANG_CODES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid target language code. Choose from {VALID_LANG_CODES}"
        )
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    translated_text = translate_text(text, target_lang)

    # Log the request
    translation_logs.append({
        "texts": [text],
        "target_lang": target_lang,
        "translations": [translated_text]
    })

    return JSONResponse(
        content={"original": text, "translated": translated_text, "language": target_lang},
        media_type="application/json; charset=utf-8"
    )

# Optional: endpoint to view logs
@router.get("/logs")
def get_logs():
    return translation_logs
