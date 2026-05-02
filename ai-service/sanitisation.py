import re
from flask import request, jsonify

# List of dangerous patterns to block
INJECTION_PATTERNS = [
    r"drop\s+table",
    r"select\s+\*",
    r"insert\s+into",
    r"delete\s+from",
    r"union\s+select",
    r"<script>",
    r"</script>",
    r"javascript:",
    r"ignore\s+previous\s+instructions",
    r"ignore\s+all\s+instructions",
    r"reveal\s+system\s+prompt",
    r"you\s+are\s+now",
    r"act\s+as\s+",
    r"--",
    r";\s*drop",
]

def sanitise_input(text):
    """
    Check input text for dangerous patterns.
    Returns (is_safe, reason)
    """
    if not text or text.strip() == "":
        return False, "Input cannot be empty"

    if len(text) > 5000:
        return False, "Input too long. Maximum 5000 characters allowed"

    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)

    # Check for injection patterns
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return False, f"Dangerous input detected. Request blocked for security."

    return True, clean_text


def sanitise_request_body(data, fields_to_check):
    """
    Sanitise multiple fields in a request body dict.
    Returns (is_safe, errors_or_clean_data)
    """
    cleaned = {}
    for field in fields_to_check:
        value = data.get(field, "")
        if value:
            is_safe, result = sanitise_input(str(value))
            if not is_safe:
                return False, {"error": result, "field": field}
            cleaned[field] = result
        else:
            cleaned[field] = value
    return True, cleaned