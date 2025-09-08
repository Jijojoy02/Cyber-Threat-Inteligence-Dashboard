# CTI Dashboard (Flask + React + SQLite, VirusTotal & AbuseIPDB)

A stable, minimal CTI dashboard:
- **Backend:** Flask + SQLite (persists lookups)
- **Frontend:** React + Vite
- **Integrations:** VirusTotal (search), AbuseIPDB (IP reputation)

No MongoDB. No Redis. Works on Windows/Mac/Linux with Docker.

## 1) Prereqs
- Docker Desktop (or Docker + Compose v2)
- VirusTotal & AbuseIPDB API keys

## 2) Configure API keys
Create a `.env` file at the project root (copy from `.env.example`):
```
VT_API_KEY=your_virustotal_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_api_key
```

## 3) Run (Docker)
```bash
docker compose up --build
```
- Frontend: http://localhost:3000
- Backend:  http://localhost:5000/api

## 4) Manual run (optional, no Docker)

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Runs at http://localhost:5000

### Frontend
```bash
cd frontend
npm install
# ensure .env has VITE_API_BASE=http://localhost:5000/api if needed
npm run dev
```
Runs at http://localhost:3000
