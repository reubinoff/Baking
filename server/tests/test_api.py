import pytest
import schemathesis
from fastapi.testclient import TestClient
from schemathesis.checks import ALL_CHECKS

from hypothesis import settings, HealthCheck

from baking.main import app


schemathesis.fixups.install(["fast_api"])

schema = schemathesis.from_asgi("/docs/openapi.json", app, base_url="/")


# @pytest.fixture(scope="session")
# def token():
#     client = TestClient(app)
#     response = client.post(
#         "/api/v1/default/auth/register",
#         json={"email": "test@example.com", "password": "test123"},
#     )
#     assert response.status_code == 200
#     return response.json()["token"]


@schema.parametrize()
@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
def test_api(db, case):
    # def test_api(db, token, case):
    case.headers = case.headers or {}
    # case.headers["Authorization"] = f"Bearer {token}"
    response = case.call_asgi(base_url="http://testserver/")
    case.validate_response(response, checks=ALL_CHECKS)
