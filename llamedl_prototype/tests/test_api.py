import pytest

from llame.api import LlamedlAPI


@pytest.fixture
def api():
    return LlamedlAPI()
