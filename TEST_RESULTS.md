# Test Results

Last local verification:

```text
............                                                             [100%]
12 passed in 0.79s
```

Coverage represented by the test suite:

- User registration
- Login
- Protected endpoint rejection without JWT
- JWT logout revocation
- Germany FREE ETF eligibility
- Germany PREMIUM expanded eligibility
- UAE FREE country restriction
- ETF retrieval
- Investment calculation and portfolio update
- Transaction history creation
- Fraud/risk calculation
- Rule-based financial insight
- Cross-user portfolio IDOR protection
- Cross-user transaction IDOR protection
- Audit events for unauthorized access attempts

Run locally:

```bash
cd backend
PYTHONPATH=. pytest -q ../tests
```
