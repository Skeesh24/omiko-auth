from httpx import codes
from testconfig import testconfig


def test_of_helthy():
    with testconfig.get_client() as client:
        response = client.get("")
    
    assert response.status_code == codes.OK
