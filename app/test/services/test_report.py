import pytest


@pytest.fixture
def report_uri():
    return '/report/'


def test_get_report(client, report_uri):
    response = client.get(f'{report_uri}')
    pytest.assume(response.status.startswith('200'))