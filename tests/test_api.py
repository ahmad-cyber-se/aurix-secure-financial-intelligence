from conftest import register_user


def test_registration_and_login(client):
    headers = register_user(client)
    me = client.get("/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["name"] == "Shahan"

    login = client.post(
        "/auth/login",
        json={"email": "shahan@example.com", "password": "StrongPass123!"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"


def test_protected_endpoint_rejects_unauthenticated_request(client):
    response = client.get("/portfolio")
    assert response.status_code == 401


def test_etf_retrieval_respects_country_and_subscription(client):
    free_headers = register_user(client, email="free@example.com", country="Germany", plan="FREE")
    free_etfs = client.get("/etfs", headers=free_headers)
    assert free_etfs.status_code == 200
    assert len(free_etfs.json()) == 3

    premium_headers = register_user(client, email="premium@example.com", country="Germany", plan="PREMIUM")
    premium_etfs = client.get("/etfs", headers=premium_headers)
    assert premium_etfs.status_code == 200
    assert len(premium_etfs.json()) == 6


def test_investment_updates_portfolio_and_transaction_history(client):
    headers = register_user(client)
    etfs = client.get("/etfs", headers=headers).json()
    etf_id = etfs[0]["id"]

    before = client.get("/portfolio", headers=headers).json()
    response = client.post("/investments", headers=headers, json={"etf_id": etf_id, "amount": "200.00"})
    assert response.status_code == 201, response.text
    after = response.json()["portfolio"]

    assert float(before["cash"]) - float(after["cash"]) == 200.0
    assert float(after["etfs"]) - float(before["etfs"]) == 200.0
    assert float(after["total_value"]) == float(before["total_value"])

    history = client.get("/transactions", headers=headers)
    assert history.status_code == 200
    assert history.json()[0]["type"] == "ETF_BUY"


def test_logout_revokes_token(client):
    headers = register_user(client)
    logout = client.post("/auth/logout", headers=headers)
    assert logout.status_code == 200
    assert client.get("/users/me", headers=headers).status_code == 401


def test_idor_user_cannot_access_another_users_portfolio_or_transactions(client):
    attacker_headers = register_user(client, email="attacker@example.com", name="Attacker")
    victim_headers = register_user(client, email="victim@example.com", name="Victim")
    victim_id = client.get("/users/me", headers=victim_headers).json()["id"]

    portfolio_attempt = client.get(f"/users/{victim_id}/portfolio", headers=attacker_headers)
    transaction_attempt = client.get(f"/users/{victim_id}/transactions", headers=attacker_headers)

    assert portfolio_attempt.status_code == 403
    assert transaction_attempt.status_code == 403

    audit = client.get("/audit-logs", headers=attacker_headers)
    assert audit.status_code == 200
    actions = [row["action"] for row in audit.json()]
    assert actions.count("UNAUTHORIZED_ACCESS_ATTEMPT") >= 2
