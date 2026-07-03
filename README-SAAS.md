# Advanced HVAC AI v2 — React + FastAPI SaaS Architecture

## क्यों यह बदलाव

Streamlit हर click पर पूरी Python script दोबारा चलाता है — latency ज़्यादा, scale करना मुश्किल,
proper REST API नहीं। यह नया version बिल्कुल **KBCD जैसी architecture** पर बना है:

- **Backend**: FastAPI (Python) — हर calculator का अपना REST endpoint, तेज़ JSON responses
- **Frontend**: React + TypeScript + Vite — तुरंत load होने वाला SPA, कोई full-page reload नहीं
- **Deployment**: दो अलग Docker containers (frontend, backend), Nginx से serve

सारे calculation formulas **advanced-hvac-ai के असली, audit किए हुए modules से बिल्कुल वैसे ही copy** किए गए हैं — कोई formula नहीं बदला, सिर्फ engine बदला है।

## Structure

```
hvac-saas/
├── backend/
│   ├── app/
│   │   ├── main.py                 FastAPI app entry
│   │   ├── services/                असली calculation logic (10 modules)
│   │   ├── schemas/requests.py      Pydantic request models
│   │   └── routers/                 API endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── calculatorConfig.ts      हर calculator की field-definition
│   │   ├── pages/                   हर calculator + Report + AI Assistant की page
│   │   ├── components/Sidebar.tsx
│   │   └── api/                     API client + Report state
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.snippet.yml
```

## Local Test (WSL में, deploy से पहले)

**Backend:**
```bash
cd hvac-saas/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=आपकी-key" > .env
uvicorn app.main:app --reload --port 8010
```
Browser में `http://localhost:8010/docs` खोलकर सारे endpoints test कर सकते हैं (FastAPI अपने-आप interactive API docs बना देता है)।

**Frontend** (नए terminal में):
```bash
cd hvac-saas/frontend
npm install
npm run dev
```
`http://localhost:5173` पर UI खुल जाएगा। Local dev में frontend backend से सीधे बात नहीं कर पाएगा जब तक `vite.config.ts` में proxy न जोड़ें, या `.env` में `VITE_API_URL=http://localhost:8010/api` सेट करें:
```bash
echo "VITE_API_URL=http://localhost:8010/api" > .env
```

## Server Deploy (Docker)

1. दोनों folders (`backend/`, `frontend/`) को अपने GitHub repo में push करें
2. Server पर clone/pull करें
3. `backend/.env` बनाएं (ANTHROPIC_API_KEY के साथ)
4. `docker-compose.snippet.yml` का content अपने मुख्य `docker-compose.yml` में जोड़ें
5. Build करें: `sudo docker compose up -d --build hvac-backend hvac-frontend`
6. पुराने Streamlit `hvac-ai` container को हटाएं और Nginx को नए port (3001) पर point करें

## Port Reference

| Service | Port |
|---|---|
| hvac-backend (FastAPI) | 8010 |
| hvac-frontend (Nginx+React) | 3001 |
| पुराना hvac-ai (Streamlit, replace होगा) | 8503 |

## अगला कदम

पूरा code तैयार है। अगले संदेश में मैं आपको step-by-step deployment guide दूंगा — GitHub push से लेकर server पर live करने तक, बिल्कुल वैसे ही जैसे advanced-hvac-ai किया था।
