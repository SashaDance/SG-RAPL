from services_api import actual_state
import pytest
from tests.data import test_cases


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    response = actual_state.chain.invoke(test_case.request.json())
    print("---------------------pred----------------------")
    print(response)
    print("---------------------target------------------------")
    print(test_case.response)
    assert response.json() == test_case.response.json()
