# redback-smartbike-mobile-backend
new separated backend repo set up in 2025T3 as the frontend moved from flutter to react over 2025, and the main mobile repo contains both past frontend and backend. this will be used to establish the new connected backend

## Setup

```bash
pip install -r requirements-dev.txt
cd backend
cp .env.example .env   # then set SECRET_KEY (generate command is in the file)
python manage.py migrate
python manage.py runserver
```

Run tests: `python manage.py test` (from `backend/`)
