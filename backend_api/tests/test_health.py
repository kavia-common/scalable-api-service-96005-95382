from fastapi import status

def test_health_requires_auth(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED

def test_health_ok(client, auth_headers):
    res = client.get("/", headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
