import pytest
from services_api import llm_vicuna13b
from tests.data import test_cases


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    response = llm_vicuna13b.chain.invoke(test_case.request.json())
    assert test_case.response_comparator(response, test_case.response)
