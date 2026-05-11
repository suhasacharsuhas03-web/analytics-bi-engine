# DEMO DAY — Security Talking Points
## AI Developer 3: Suhas

## MY 60-SECOND SECURITY SECTION

Point 1 - Input Sanitisation:
Every input passes through sanitisation middleware I built.
It blocks SQL injection, XSS, and prompt injection.
Demo: POST to /test-security with script tag - shows 400 blocked.

Point 2 - Rate Limiting:
flask-limiter blocks any IP exceeding 30 requests per minute.
After 30 requests, returns 429 Too Many Requests.
Protects Groq API quota and prevents denial of service.

Point 3 - Security Headers:
flask-talisman adds security headers to every response.
X-Content-Type-Options, X-Frame-Options, X-XSS-Protection.
Demo: GET /health shows all headers present.

Point 4 - OWASP ZAP Results:
Ran automated ZAP scan - found 2 medium findings.
Both fixed - missing headers and CORS misconfiguration.
Re-scan confirmed zero Critical and zero High remaining.

## Q&A ANSWERS

Q: What does the AI service do?
A: 4 AI endpoints using Groq LLaMA-3.3-70b - describe, recommend, categorise, generate-report.

Q: What AI model are you using?
A: Groq LLaMA-3.3-70b - fast, free tier, no credit card needed.

Q: What is RAG?
A: Retrieval Augmented Generation - retrieve relevant docs from ChromaDB vector database,
inject as context into the prompt, makes answers more accurate.

Q: What security measures did you implement?
A: Input sanitisation, rate limiting at 30 req/min, security headers, OWASP ZAP scan with all findings fixed.
