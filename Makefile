.PHONY: up down test backend-dev frontend-dev

up:
	docker compose up --build

down:
	docker compose down

test:
	cd backend && PYTHONPATH=. pytest -q ../tests

backend-dev:
	cd backend && alembic upgrade head && uvicorn app.main:app --reload --port 8000

frontend-dev:
	cd frontend && npm run dev
