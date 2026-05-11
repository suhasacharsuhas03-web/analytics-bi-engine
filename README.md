# Tool-78 — Analytics and BI Engine
**Internship Capstone Project | Sprint: 14 April - 9 May 2026**

## Project Overview
An AI-powered Analytics and Business Intelligence Engine built with
Java Spring Boot, Python Flask, Groq LLaMA-3.3-70b, PostgreSQL, Redis, and React.

## Architecture
## Team
7 Members | AI Developer 3: Suhas (Security + AI Service)

## Prerequisites
- Docker and Docker Compose
- Python 3.11
- Java 17
- Node.js 18+
- Groq API key (free at https://console.groq.com)

## Setup Instructions
1. Clone the repository
2. Copy .env.example to .env and fill in your values
3. Add your GROQ_API_KEY to .env
4. Run: docker-compose up --build
5. Access frontend at http://localhost
6. Access backend API at http://localhost:8080/swagger-ui.html
7. Access AI service at http://localhost:5000/health

## AI Service Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Service health check |
| /describe | POST | Generate record description |
| /recommend | POST | Get 3 actionable recommendations |
| /categorise | POST | Classify record into category |
| /generate-report | POST | Generate full analytics report |
| /test-security | POST | Test input sanitisation |

## Security
- Input sanitisation — blocks SQL injection, XSS, prompt injection
- Rate limiting — 30 requests/minute via flask-limiter
- Security headers — flask-talisman (X-Content-Type-Options, X-Frame-Options)
- OWASP ZAP scanned — zero Critical/High findings
- See SECURITY.md for full security documentation

## Running Tests
```bash
cd ai-service
python -m pytest test_ai_service.py -v
```
10 tests, all passing, Groq API mocked.

## Environment Variables
See .env.example for all required variables.
