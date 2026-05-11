from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from sanitisation import sanitise_input
from services.groq_client import call_groq

categorise_bp = Blueprint('categorise', __name__)

def load_prompt(filename):
    with open(f"prompts/{filename}", "r") as f:
        return f.read()

@categorise_bp.route('/categorise', methods=['POST'])
def categorise():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    title = data.get('title', '')
    description = data.get('description', '')
    is_safe, cleaned = sanitise_input(str(title) + " " + str(description))
    if not is_safe:
        return jsonify({"error": cleaned, "blocked": True}), 400
    prompt_template = load_prompt("categorise_prompt.txt")
    prompt = prompt_template.replace("{title}", str(title)).replace("{description}", str(description))
    result, is_fallback = call_groq([{"role": "user", "content": prompt}], temperature=0.2)
    try:
        parsed = json.loads(result)
    except Exception:
        parsed = {"category": "OTHER", "confidence": 0.5, "reasoning": result}
    parsed["generated_at"] = datetime.utcnow().isoformat()
    parsed["is_fallback"] = is_fallback
    return jsonify(parsed), 200
