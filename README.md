# HOPn / AURIX — Secure Financial Intelligence Prototype

A 24-hour technical evaluation MVP implementing the requested AURIX architecture using **Python/FastAPI**, **PostgreSQL**, **React/Next.js**, **JWT authentication**, **OpenAPI/Swagger**, **automated tests**, and **Docker Compose**.

> **Simulation only:** No real funds, securities, brokerage, payment rail, custody service, or live market feed is connected. The financial insight endpoint is deterministic and rule-based.

## 1. Project overview

The prototype demonstrates how a secure financial application can manage users, ETF products, country/subscription eligibility, portfolios, simulated investments, transactions, audit records, fraud/risk scoring, and rule-based financial insights.

Implemented evaluation requirements include:

- Registration, login, logout, password hashing, authentication middleware, protected endpoints
- User profile: name, email, country, subscription plan, KYC status, created timestamp
- ETF catalogue with six realistic mock products
- Country + subscription eligibility service for Germany and UAE
- Portfolio summary for Gold, Silver, ETFs, Cash, and Other
- Simulated ETF investment flow
- Transaction history
- SQL injection protection through parameterized ORM queries
- Authorization / IDOR protection
- Input validation through Pydantic
- Audit logging for login, failed login, investment, portfolio/profile changes, and denied access
- Rule-based fraud/anomaly scoring (LOW/MEDIUM/HIGH)
- Rule-based financial insight endpoint
- Swagger/OpenAPI documentation
- Required Next.js screens
- Unit, API, and security tests
- Docker Compose with frontend, backend, PostgreSQL

## 2. Architecture

```text
Frontend (Next.js / React)
        ↓
REST API (FastAPI)
        ↓
Business / Service Layer
        ↓
PostgreSQL
        ↓
Security / Audit Layer
```

Detailed diagram: [`ARCHITECTURE.md`](ARCHITECTURE.md)

Backend service separation:

- `EligibilityService` — country/subscription ETF access
- `PortfolioService` — portfolio totals and allocations
- `InvestmentService` — investment workflow and consistency
- `FraudRiskService` — deterministic risk scoring
- `InsightService` — rule-based portfolio observation/recommendation
- `AuditService` — traceability and security events

## 3. Technology choices

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- Argon2 password hashing (`argon2-cffi`)
- PyJWT
- Alembic migrations

Why FastAPI: it matches the requested preferred stack and provides typed request validation plus automatic OpenAPI/Swagger documentation.

### Database

- PostgreSQL 17
- Local development: Dockerized PostgreSQL
- Hosted evaluation option: Neon PostgreSQL

The application uses a pooled PostgreSQL URL for normal web traffic and supports a separate direct URL for migrations.

### Frontend

- Next.js 16
- React 19
- TypeScript
- App Router

### Testing

- pytest
- FastAPI TestClient
- SQLite isolated test database for fast deterministic test execution

### DevOps

- Dockerfiles for frontend/backend
- `docker-compose.yml`
- `.env.example`
- Git-safe `.gitignore`

## 4. Installation

### Option A — Docker Compose (recommended)

Requirements:

- Docker
- Docker Compose

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder secrets, especially:

```env
POSTGRES_PASSWORD=replace_me
JWT_SECRET=replace_with_at_least_32_random_bytes
```

Then run:

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:3000`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Option B — Run manually

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## 5. Environment variables

See `.env.example`.

Key variables:

```env
DATABASE_URL=postgresql+psycopg://...
DATABASE_URL_MIGRATIONS=postgresql+psycopg://...
JWT_SECRET=...
JWT_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Do **not** commit `.env`, passwords, database credentials, private keys, tokens, or API keys.

## 6. Database setup

The schema is versioned through Alembic.

Apply migrations:

```bash
cd backend
alembic upgrade head
```

Core tables:

```text
users
etfs
eligibility_rules
portfolios
portfolio_assets
transactions
audit_logs
revoked_tokens
```

Reference ETF and eligibility data is seeded automatically at API startup when missing.

### Seeded ETFs

- MSCI World
- S&P 500
- Nasdaq-100
- FTSE All-World
- Emerging Markets
- Euro Stoxx 50

### Eligibility rules

```text
Germany + FREE    → IWDA, CSPX, EUE
Germany + PREMIUM → all six
UAE + FREE        → IWDA, CSPX, VWRL
UAE + PREMIUM     → all six
```

The rules are evaluated in the backend service layer, never hard-coded into the UI.

## 7. How to run

After startup:

1. Open `http://localhost:3000/register`
2. Create a Germany or UAE user
3. Log in
4. Review Dashboard
5. Open ETF Catalogue
6. View ETF Details
7. Execute a simulated ETF investment
8. Review Portfolio update
9. Review Transaction History
10. Review Security / Activity audit logs
11. Open Swagger at `http://localhost:8000/docs`

## 8. API documentation

FastAPI automatically generates OpenAPI and Swagger.

### Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/logout
```

### User

```text
GET   /users/me
PATCH /users/me
GET   /users/{user_id}/portfolio
GET   /users/{user_id}/transactions
```

The two user-ID routes exist specifically to demonstrate object-level authorization / IDOR protection.

### ETFs

```text
GET /etfs
GET /etfs/{etf_id}
```

### Portfolio

```text
GET /portfolio
GET /portfolio/assets
GET /portfolio/insights
```

### Investment / Transactions

```text
POST /investments
GET  /transactions
```

### Audit

```text
GET /audit-logs
```

### System

```text
GET /health
```

## 9. Testing

Run:

```bash
cd backend
PYTHONPATH=. pytest -q ../tests
```

Current local result:

```text
12 passed
```

The tests cover:

- ETF eligibility
- Country restrictions
- Subscription restrictions
- Investment calculation
- Fraud/risk calculation
- Registration
- Login
- Protected endpoint
- ETF retrieval
- Investment
- Logout revocation
- Unauthorized cross-user portfolio access
- Unauthorized cross-user transaction access
- Audit creation for IDOR attempts

Full evidence: [`TEST_RESULTS.md`](TEST_RESULTS.md)

## 10. Security considerations

### Password security

Passwords are hashed using Argon2 and are never returned by API response models.

### Authentication

- Signed JWT access tokens
- Issuer and audience validation
- Expiration validation
- JWT ID (`jti`)
- Server-side revocation list for logout

### SQL injection

Database access uses SQLAlchemy expression APIs and bound parameters. User input is never concatenated into raw SQL.

### Authorization / IDOR

Private portfolio and transaction access is tied to the authenticated principal. A user attempting:

```text
/users/<another-user-id>/portfolio
```

receives HTTP 403 and the event is recorded as `UNAUTHORIZED_ACCESS_ATTEMPT`.

### Input validation

FastAPI/Pydantic validates:

- Email addresses
- Password length
- UUIDs
- Positive investment amounts
- Enum values
- Pagination bounds

### Sensitive information exposure

- Password hashes are excluded from response schemas
- Secrets are environment-only
- `.env` is gitignored
- Error messages avoid revealing password validity separately from account validity

### Audit logging

Logged events include:

- Register
- Login
- Failed login
- Logout
- Investment
- Portfolio change
- Profile change
- Unauthorized access attempt

Each audit record stores user, action, entity, entity ID, timestamp, IP address, result, and optional structured details.

### Fraud / anomaly rules

Risk inputs include:

- High transaction amount
- Percentage of available cash consumed
- Multiple transactions inside a short interval

Output:

```text
LOW
MEDIUM
HIGH
```

with an explainable reason and numeric internal score.

## 11. Known limitations

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

Key limitations:

- No real brokerage, bank, payment, custody, or market-data integration
- Mock ETF values / simulated balances
- No external KYC provider
- Germany/UAE only for eligibility demo
- Rule-based fraud engine
- Rule-based insight, not a real AI model
- No MFA, refresh-token rotation, or external SIEM in this evaluation MVP

## 12. What I would implement next with more time

1. MFA and refresh-token rotation
2. Rate limiting, login throttling, and account lockout policy
3. External KYC/AML integration
4. Real brokerage sandbox/order lifecycle
5. Live market data and FX conversion
6. Configurable policy/rules engine rather than seeded eligibility rows only
7. Fraud case management and behavioral baselines
8. Dedicated immutable audit export to SIEM/WORM storage
9. Role-based administration
10. CI/CD with security scanning, dependency scanning, migration gates, and deployment environments
11. PostgreSQL row-level security as a defense-in-depth layer
12. Observability: structured logs, traces, metrics, alerts
13. API rate quotas and idempotency keys for financial actions
14. Contract tests and browser end-to-end tests

## Demo

A suggested 3–5 minute walkthrough is provided in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).

## Repository structure

```text
.
├── README.md
├── ARCHITECTURE.md
├── TEST_RESULTS.md
├── KNOWN_LIMITATIONS.md
├── DEMO_SCRIPT.md
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── Dockerfile
│   └── package.json
└── tests/
    ├── test_api.py
    └── test_unit_services.py
```
