import re
import html

# Patterns that indicate prompt injection or SQL injection
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard.*instructions",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"reveal.*prompt",
    r"show.*system prompt",
    r"drop\s+table",
    r"select\s+\*\s+from",
    r"insert\s+into",
    r"delete\s+from",
    r"union\s+select",
    r";\s*--",
    r"<script",
    r"javascript:",
    r"onerror=",
    r"onload=",
]

def sanitise_input(text: str):
    """
    Sanitise user input.
    Returns (is_safe: bool, result: str)
    - If safe: (True, cleaned_text)
    - If unsafe: (False, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Input must be a non-empty string"

    if len(text) > 2000:
        return False, "Input exceeds maximum length of 2000 characters"

    # Check for injection patterns
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return False, f"Blocked: potentially malicious input detected"

    # Strip HTML tags
    cleaned = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    cleaned = html.unescape(cleaned)

    # Remove null bytes
    cleaned = cleaned.replace('\x00', '')

    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    if not cleaned:
        return False, "Input is empty after sanitisation"

    return True, cleaned