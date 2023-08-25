from httpx import codes
from testconfig import testconfig


PREFIX = "/user"


def test_user_deletion():
    with testconfig.get_client() as client:
        response = client.delete(
            PREFIX, headers={"Authorization": "Bearer " + testconfig.ACCESS}
        )

    assert response.status_code == codes.NO_CONTENT
