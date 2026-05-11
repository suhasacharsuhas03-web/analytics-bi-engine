# DEMO DAY — Security Talking Points
## AI Developer 3: Suhas

---

## MY 60-SECOND SECURITY SECTION (Demo Day)

"I was responsible for all security in the AI service. Let me show you four things."

---

### Point 1: Input Sanitisation
**What to say:**
"Every input to the AI service passes through a sanitisation middleware I built.
It blocks SQL injection, XSS attacks, and prompt injection attempts.
Watch this — I will send a script tag and show you it gets blocked with a 400 error."

**Live demo command:**
POST /test-security with input: "<script>alert(1)</script>"
Expected: {"blocked": true, "error": "Blocked: potentially malicious input detected"}

---

### Point 2: Rate Limiting
**What to say:**
"I implemented rate limiting using flask-limiter.
No IP can exceed 30 requests per minute. After that, they get a 429 Too Many Requests.
This protects our Groq API quota and prevents denial of service attacks."

**Live demo command:**
Run 35 rapid requests — show 200s turning into 429s after 30

---

### Point 3: Security Headers
**What to say:**
"I added flask-talisman which automatically adds security headers to every response.
X-Content-Type-Options prevents MIME sniffing attacks.
X-Frame-Options prevents clickjacking.
X-XSS-Protection adds browser-level XSS filtering."

**Live demo command:**
GET /health — show headers in response:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block

---

### Point 4: OWASP ZAP Results
**What to say:**
"I ran OWASP ZAP automated security scans on the application.
The initial scan found two medium severity findings — missing headers and CORS misconfiguration.
Both were fixed. The re-scan confirmed zero Critical and zero High findings remaining.
All findings are documented in SECURITY.md which I can show you now."

**Point to:** SECURITY.md Section 3 — ZAP Scan Results

---

## Q&A ANSWERS — Memorise These

**Q: What does the AI service do?**
A: "It provides 4 AI endpoints powered by Groq LLaMA-3.3-70b — describe, recommend,
categorise, and generate-report. Each takes analytics record data and returns
AI-generated insights."

**Q: What AI model are you using?**
A: "We use Groq's LLaMA-3.3-70b model via their free API. It is fast, accurate,
and requires no credit card for the free tier."

**Q: What is RAG?**
A: "RAG stands for Retrieval Augmented Generation. It means instead of relying only
on the AI model's training data, we first retrieve relevant documents from ChromaDB
vector database and inject them as context into the prompt. This makes answers
more accurate and specific to our data."

**Q: What security measures did you implement?**
A: "Four main measures — input sanitisation blocking injections, rate limiting at
30 requests per minute, security headers via flask-talisman, and OWASP ZAP
scanning with all findings resolved."

---

## SECURITY.md QUICK REFERENCE
- Threats documented: 10
- Tests conducted: 13
- All tests: PASS
- Critical findings: 0
- High findings: 0
- Medium findings fixed: 2
