# 3–5 Minute Demo Script

## 0:00–0:20 — Architecture
Show `ARCHITECTURE.md` and explain: Next.js frontend → FastAPI REST API → service layer → PostgreSQL → audit/security layer.

## 0:20–0:50 — Registration and login
Register a Germany FREE user. Show successful login and protected dashboard.

## 0:50–1:25 — Dashboard and portfolio
Show €10,000 portfolio with Gold 40%, Silver 15%, ETFs 35%, Cash 10%, recent transactions, and the rule-based insight.

## 1:25–1:55 — ETF eligibility
Open ETF Catalogue. Show that Germany FREE receives a limited catalogue. Change the Profile subscription to PREMIUM and return to the catalogue to show the expanded set. Mention that the rules come from the backend `eligibility_rules` table/service, not the UI.

## 1:55–2:35 — ETF details and investment
Open an ETF, then Investment. Enter an amount, submit, and show eligibility validation, cash validation, fraud scoring, portfolio update, transaction creation, and audit creation.

## 2:35–2:55 — Fraud result
Use a larger amount when cash allows or explain the deterministic thresholds. Show the LOW/MEDIUM/HIGH result and reason in transaction history.

## 2:55–3:25 — Security / IDOR
Create a second user. In Swagger, authenticate as User A and request `/users/{user_b_id}/portfolio`. Show HTTP 403. Then open Security / Activity and show `UNAUTHORIZED_ACCESS_ATTEMPT` recorded.

## 3:25–3:50 — Swagger and tests
Open `/docs`, briefly show the required endpoints, then show `TEST_RESULTS.md` or terminal output with `12 passed`.

## 3:50–4:10 — Limitations
State explicitly: simulated funds, mock ETF data, rule-based insight, no real brokerage/KYC integration. Mention next steps from README.
