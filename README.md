# PlateWise

PlateWise is a multi-tenant hostel meal intelligence platform. It helps teams plan service, capture attendance, measure waste, and make evidence-based kitchen decisions.

## Included in this build

- Django REST API with tenant-scoped access through `X-Hostel-Id` and membership checks.
- Student directory plus safe CSV roster preview and idempotent transactional commit.
- Meal session lifecycle (`draft → open → closed`) with quantity validation.
- Duplicate-safe attendance backed by a database uniqueness constraint.
- Daily operational summary endpoint and a separate React/Vite operations dashboard.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

## API

All operational API calls require an authenticated user and an `X-Hostel-Id` header. Primary routes are:

- `GET/POST /api/v1/students/`
- `POST /api/v1/students/imports/preview`
- `POST /api/v1/students/imports/commit`
- `GET/POST /api/v1/meal-sessions/`
- `POST /api/v1/meal-sessions/{id}/attendance`
- `GET /api/v1/analytics/summary?date=YYYY-MM-DD`
