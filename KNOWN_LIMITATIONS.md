# Known Limitations

1. This is an evaluation prototype. No real money, brokerage, custody, bank, or exchange integration exists.
2. ETF market prices are not live; portfolio values are simulated, as permitted by the brief.
3. The financial insight endpoint is deliberately rule-based and clearly reports `RULE-BASED`; it does not claim to use a real AI model.
4. KYC state is modeled but no external KYC provider is integrated.
5. Only Germany and UAE eligibility rules are seeded for the evaluation scenario.
6. The fraud engine is deterministic and intentionally simple; a production platform would require configurable rules, behavioral baselines, velocity windows, device intelligence, and case management.
7. Access tokens use a short-lived JWT plus server-side revocation on logout. A production system would add refresh-token rotation, MFA, rate limiting, device/session management, and stronger account recovery controls.
8. The prototype does not include real-time securities valuation, FX conversion, corporate actions, tax handling, settlement states, or brokerage order lifecycle management.
9. Audit records demonstrate traceability but are not cryptographically immutable or exported to a dedicated SIEM/WORM system.
10. Deployment manifests are Docker Compose for the evaluation; production would add CI/CD, secret management, health monitoring, TLS termination, backups, alerts, and environment-specific infrastructure.
