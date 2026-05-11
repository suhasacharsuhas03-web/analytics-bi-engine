from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from sanitisation import sanitise_input
from services.groq_client import call_groq

report_bp = Blueprint('report', __name__)

def load_prompt(filename):
    with open(f"prompts/{filename}", "r") as f:
        return f.read()

@report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    raw_data = str(data.get('data', data))

    is_safe, cleaned = sanitise_input(raw_data[:500])
    if not is_safe:
        return jsonify({"error": cleaned, "blocked": True}), 400

    prompt_template = load_prompt("report_prompt.txt")
    prompt = prompt_template.replace("{data}", raw_data[:1500])

    result, is_fallback = call_groq([
        {"role": "user", "content": prompt}
    ], temperature=0.4, max_tokens=1000)

    try:
        report = json.loads(result)
    except Exception:
        report = {
            "title": "Analytics Report",
            "executive_summary": result,
            "overview": result,
            "top_items": [],
            "recommendations": []
        }

    report["generated_at"] = datetime.utcnow().isoformat()
    report["is_fallback"] = is_fallback

    return jsonify(report), 200