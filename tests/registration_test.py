from httpx import codes
from testconfig import testconfig


PREFIX = "/user"


def test_user_registration():
    with testconfig.get_client() as client:
        response = client.post(
            PREFIX,
            json={"username": "josh", "password": "cancel"},
        )

    assert response.status_code == codes.CREATED
