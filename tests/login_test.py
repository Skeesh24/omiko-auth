from httpx import codes
from testconfig import testconfig


ROUTE = "/auth"


def test_login():
    with testconfig.get_client(ROUTE) as client:
        response = client.post(
            "/login",
            data={"username": "jesus", "password": "christ"},
        )

    assert response.status_code == codes.OK
