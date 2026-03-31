# Account Health Dashboard

A simple dashboard for viewing B2B customer accounts. Displays account health scores, ARR, industry, ownership, and contact history.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React, TypeScript, Vite

## Getting Started

### Backend

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database
python seed.py

# Start the API server
uvicorn app.main:app --reload
```

The API will be running at `http://localhost:8000`. The SQLite database (`accounts.db`) is created automatically when you run the seed script or start the server.

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be running at `http://localhost:5173`.

### Running Backend Tests

```bash
cd backend
pytest
```
