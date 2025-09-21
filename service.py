from deep_translator import GoogleTranslator

# In-memory log to store all translation requests
translation_logs = []

def translate_text(text: str, target_lang: str) -> str:
    """Translate a single text."""
    try:
        return GoogleTranslator(target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation error: {str(e)}]"

def translate_bulk(texts: list, target_lang: str) -> list:
    """Translate multiple texts and log the request."""
    translations = [translate_text(t, target_lang) for t in texts]

    # Save log
    translation_logs.append({
        "texts": texts,
        "target_lang": target_lang,
        "translations": translations
    })

    return translations
