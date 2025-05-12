import pytest
from services_api import seg_and_track
from .tests.data import test_cases


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test_segmentor_api(test_case):
    response = seg_and_track.chain.invoke(test_case.request.json())
    assert test_case.response_comparator(response.json(), test_case.response.json())
