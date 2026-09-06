# 3–5 Minute Demo Script

## 0:00–0:20 — Architecture
Show `ARCHITECTURE.md` and explain: Next.js frontend → FastAPI REST API → service layer → PostgreSQL → audit/security layer.

## 0:20–0:50 — Registration and login
Register a Germany FREE user or a UAE user. Show the successful login and the protected dashboard. Keep the flow simple and avoid any claims of a live production deployment.

## 0:50–1:25 — Dashboard and portfolio
Open the dashboard and show the seeded demo portfolio state, recent transactions, and the rule-based insight panel. The repo uses a simulated cash baseline and deterministic portfolio values for the evaluation, not live market price data.

## 1:25–1:55 — ETF eligibility
Open the ETF Catalogue. Show that the Germany FREE user sees the limited catalogue, while the premium rule set is represented in the profile model and backend eligibility rules. If you want to demonstrate the second rule set, update the subscription field on the Profile page and refresh; the UI supports this field in the local demo.

## 1:55–2:35 — ETF details and investment
Open an ETF, then the Investment page. Use a modest amount that matches the seeded demo balance rather than an unusually large value. Submit the transaction and show eligibility validation, available-cash validation, fraud scoring, portfolio update, transaction creation, and audit creation.

## 2:35–2:55 — Fraud result
Use a transaction sized consistently with the demo balance to keep the fraud demonstration realistic. For example, a larger amount that uses a meaningful share of the starter cash will produce a LOW/MEDIUM/HIGH result based on the deterministic risk rules; the reason is visible in the transaction history and audit trail.

## 2:55–3:25 — Security / IDOR
Create a second user. In Swagger, authenticate as User A and request `/users/{user_b_id}/portfolio`. Show the unauthorized response and then open the Security / Activity page to show the `UNAUTHORIZED_ACCESS_ATTEMPT` audit entry.

## 3:25–3:50 — Swagger and tests
Open `/docs` and briefly show the required endpoints, then show `TEST_RESULTS.md` or the terminal output from the verification run: `12 passed, 2 warnings in 1.65s`.

## 3:50–4:10 — Limitations
State clearly: this is a simulated demo, the ETF data is mock, the insight engine is deterministic and rule-based, and there is no live brokerage/KYC integration. Mention that the local repo is intended for evaluation and not a production-ready fintech platform.
