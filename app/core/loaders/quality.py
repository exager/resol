def validate_extraction(text: str, *, min_chars: int = 300):
    if len(text) < min_chars:
        raise ValueError("extracted_text_too_short")
