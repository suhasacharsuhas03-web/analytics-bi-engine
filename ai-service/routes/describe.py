from flask import Blueprint, request, jsonify
from datetime import datetime
from sanitisation import sanitise_input
from services.groq_client import call_groq

describe_bp = Blueprint('describe', __name__)

def load_prompt(filename):
    with open(f"prompts/{filename}", "r") as f:
        return f.read()

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    title = data.get('title', '')
    status = data.get('status', '')
    score = data.get('score', '')
    context = data.get('context', '')
    is_safe, cleaned = sanitise_input(str(title) + " " + str(context))
    if not is_safe:
        return jsonify({"error": cleaned, "blocked": True}), 400
    prompt_template = load_prompt("describe_prompt.txt")
    prompt = prompt_template.replace("{title}", str(title)).replace("{status}", str(status)).replace("{score}", str(score)).replace("{context}", str(context))
    result, is_fallback = call_groq([{"role": "user", "content": prompt}], temperature=0.3)
    return jsonify({"description": result, "generated_at": datetime.utcnow().isoformat(), "is_fallback": is_fallback}), 200

@describe_bp.route('/recommend', methods=['POST'])
def recommend():
    import json
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    title = data.get('title', '')
    status = data.get('status', '')
    score = data.get('score', '')
    description = data.get('description', '')
    is_safe, cleaned = sanitise_input(str(title) + " " + str(description))
    if not is_safe:
        return jsonify({"error": cleaned, "blocked": True}), 400
    prompt_template = load_prompt("recommend_prompt.txt")
    prompt = prompt_template.replace("{title}", str(title)).replace("{status}", str(status)).replace("{score}", str(score)).replace("{description}", str(description))
    result, is_fallback = call_groq([{"role": "user", "content": prompt}], temperature=0.5)
    try:
        recommendations = json.loads(result)
    except Exception:
        recommendations = [{"action_type": "REVIEW", "description": result, "priority": "MEDIUM"}]
    return jsonify({"recommendations": recommendations, "generated_at": datetime.utcnow().isoformat(), "is_fallback": is_fallback}), 200
