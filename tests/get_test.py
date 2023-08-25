from httpx import codes
from testconfig import testconfig


PREFIX = "/user"

def test_get_all_users():
    with testconfig.get_client() as client:
        response = client.get(PREFIX)

    assert response.status_code == codes.OK or response.status_code == codes.NOT_FOUND
