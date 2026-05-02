from flask import Flask, jsonify
from services.rate_limiter import init_limiter

app = Flask(__name__)

# Initialize rate limiter
limiter = init_limiter(app)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "Analytics BI Engine - AI Service",
        "developer": "Suhas - AI Developer 3",
        "version": "1.0.0"
    }), 200

# Test sanitisation endpoint
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
        return jsonify({
            "error": result,
            "blocked": True
        }), 400

    return jsonify({
        "message": "Input is safe",
        "cleaned_input": result,
        "blocked": False
    }), 200

# Handle rate limit exceeded
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Too many requests",
        "message": "Rate limit exceeded. Please wait before trying again.",
        "retry_after": "60 seconds"
    }), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)