import pytest
import respx


@pytest.fixture
def pytilz_loaded():
    yield True


@pytest.fixture(autouse=True)
def respx_catch_all():
    with respx.mock as respx_mock:
        yield respx_mock
