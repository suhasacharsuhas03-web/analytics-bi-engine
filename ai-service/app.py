from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from services.rate_limiter import init_limiter
from routes.describe import describe_bp
from routes.categorise import categorise_bp
from routes.report import report_bp

app = Flask(__name__)

# Security headers — must be before CORS
talisman = Talisman(app,
    content_security_policy=False,
    force_https=False,
    strict_transport_security=False,
    x_content_type_options=True,
    x_xss_protection=True,
    frame_options='SAMEORIGIN'
)

# CORS after Talisman
CORS(app, origins=["http://localhost", "http://localhost:3000", "http://localhost:5173"])

# Rate limiter
limiter = init_limiter(app)

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(categorise_bp)
app.register_blueprint(report_bp)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "Analytics BI Engine - AI Service",
        "developer": "Suhas - AI Developer 3",
        "version": "1.0.0",
        "endpoints": ["/describe", "/recommend", "/categorise", "/generate-report"],
        "security_headers": "enabled"
    }), 200

@app.route('/test-security', methods=['POST'])
@limiter.limit("10 per minute")
def test_security():
    from flask import request
    from sanitisation import sanitise_input
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({"error": "No input provided"}), 400
    is_safe, result = sanitise_input(data['input'])
    if not is_safe:
        return jsonify({"error": result, "blocked": True}), 400
    return jsonify({"message": "Input is safe", "cleaned_input": result, "blocked": False}), 200

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Too many requests",
        "message": "Rate limit exceeded. Please wait before trying again.",
        "retry_after": "60 seconds"
    }), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
