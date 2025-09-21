from pydantic import BaseModel
from typing import List

# Request model
class TranslateRequest(BaseModel):
    texts: List[str]        # List of sentences
    target_lang: str        # ISO language code (e.g., 'hi', 'fr', 'ta')

# List of valid languages for validation
VALID_LANG_CODES = ["hi", "ta", "bn", "fr", "es", "de", "en"]  # Add more as needed
