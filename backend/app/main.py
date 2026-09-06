from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import audit, auth, etfs, investments, portfolio, transactions, users
from app.core.config import settings
from app.db.session import SessionLocal
from app.seed import seed_reference_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is versioned with Alembic. Seed only stable evaluation reference data at startup.
    with SessionLocal() as db:
        seed_reference_data(db)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Secure financial intelligence evaluation MVP. All investments are simulated; no real money, brokerage, "
        "or live market integration is used. The AI insight endpoint is explicitly rule-based."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(etfs.router)
app.include_router(portfolio.router)
app.include_router(investments.router)
app.include_router(transactions.router)
app.include_router(audit.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "aurix-api"}
