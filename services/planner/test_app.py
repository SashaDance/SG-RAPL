from services_api import planner
import pytest
from tests.data import test_cases


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    response = planner.chain.invoke(test_case.request.json())
    assert response.json() == test_case.response.json()
