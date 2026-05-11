# AI Service — Analytics and BI Engine

**Developer:** Suhas (AI Developer 3)
**Port:** 5000
**Framework:** Flask 3.x + Groq LLaMA-3.3-70b

---

## Prerequisites
- Python 3.11
- Groq API key (free at https://console.groq.com)

---

## Setup Instructions

1. Navigate to ai-service folder:
2. Install dependencies:
3. Create .env file in the project root (see .env.example):
4. Run the service:
5. Verify it is running:
---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Your Groq API key from console.groq.com | Yes |

---

## API Endpoints

### GET /health
Returns service status and available endpoints.

**Response:**
```json
{
  "status": "ok",
  "service": "Analytics BI Engine - AI Service",
  "version": "1.0.0",
  "endpoints": ["/describe", "/recommend", "/categorise", "/generate-report"]
}
```

---

### POST /describe
Generates a professional description of an analytics record.

**Request:**
```json
{
  "title": "Q1 Sales Report",
  "status": "completed",
  "score": 85,
  "context": "quarterly revenue analysis"
}
```

**Response:**
```json
{
  "description": "AI generated description here",
  "generated_at": "2026-05-11T09:00:00",
  "is_fallback": false
}
```

---

### POST /recommend
Returns 3 actionable recommendations for a record.

**Request:**
```json
{
  "title": "Q1 Sales Report",
  "status": "completed",
  "score": 85,
  "description": "quarterly revenue analysis"
}
```

**Response:**
```json
{
  "recommendations": [
    {"action_type": "IMPROVE", "description": "...", "priority": "HIGH"},
    {"action_type": "MONITOR", "description": "...", "priority": "MEDIUM"},
    {"action_type": "REVIEW", "description": "...", "priority": "LOW"}
  ],
  "generated_at": "2026-05-11T09:00:00",
  "is_fallback": false
}
```

---

### POST /categorise
Classifies a record into a business category.

**Request:**
```json
{
  "title": "Q1 Sales Report",
  "description": "quarterly revenue analysis"
}
```

**Response:**
```json
{
  "category": "FINANCIAL",
  "confidence": 0.95,
  "reasoning": "explanation here",
  "generated_at": "2026-05-11T09:00:00",
  "is_fallback": false
}
```

---

### POST /generate-report
Generates a full analytical report.

**Request:**
```json
{
  "data": {
    "title": "Q1 Sales",
    "status": "completed",
    "score": 85
  }
}
```

**Response:**
```json
{
  "title": "Report title",
  "executive_summary": "summary here",
  "overview": "detailed overview",
  "top_items": ["finding 1", "finding 2", "finding 3"],
  "recommendations": ["rec 1", "rec 2", "rec 3"],
  "generated_at": "2026-05-11T09:00:00",
  "is_fallback": false
}
```

---

### POST /test-security
Tests input sanitisation (rate limited to 10/min).

**Request:**
```json
{"input": "your test input here"}
```

---

## Security Features
- Input sanitisation middleware blocks SQL injection and prompt injection
- Rate limiting: 30 req/min globally, 10 req/min on /test-security
- Security headers via flask-talisman (X-Content-Type-Options, X-Frame-Options)
- CORS restricted to frontend origins only

---

## Tech Stack
| Component | Technology |
|-----------|------------|
| Framework | Flask 3.0 |
| AI Model | Groq LLaMA-3.3-70b |
| Rate Limiting | flask-limiter |
| Security Headers | flask-talisman |
| Input Safety | Custom sanitisation middleware |
