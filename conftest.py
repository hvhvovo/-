import os
import json
from pathlib import Path
import uuid
import pytest
from booking.client import Client

def pytest_addoption(parser):
    parser.addoption('--live', action='store_true')
    parser.addoption('--allow-write', action='store_true')
    parser.addoption('--base-url', default=os.getenv('BOOKING_BASE_URL',
        'https://restful-booker.herokuapp.com'))

def pytest_collection_modifyitems(config, items):
    for item in items:
        if 'live' in item.keywords and not config.getoption('--live'):
            item.add_marker(pytest.mark.skip(reason='Network tests require --live'))
        if 'write' in item.keywords and not config.getoption('--allow-write'):
            item.add_marker(pytest.mark.skip(reason='Writes require --allow-write'))

@pytest.fixture
def api(request):
    trace = []
    request.node._api_trace = trace
    client = Client(request.config.getoption('--base-url'), trace=trace)
    yield client
    client.session.close()

@pytest.fixture
def token(api):
    data = api.json('POST', '/auth', 200,
        json={'username': 'admin', 'password': 'password123'})
    assert isinstance(data, dict) and isinstance(data.get('token'), str) and data['token']
    return data['token']

@pytest.fixture
def owned(api, token):
    payload = {'firstname': 'qa_' + uuid.uuid4().hex[:12], 'lastname': 'Automation',
        'totalprice': 123, 'depositpaid': True,
        'bookingdates': {'checkin': '2027-05-10', 'checkout': '2027-05-12'},
        'additionalneeds': 'Breakfast'}
    result = api.json('POST', '/booking', 200, json=payload)
    assert isinstance(result, dict) and type(result.get('bookingid')) is int
    bid = result['bookingid']
    try:
        yield bid, payload, result
    finally:
        # Only this fixture's newly created ID is eligible for cleanup.
        try:
            existing = api.session.request('GET', api.base_url + f'/booking/{bid}',
                headers={'Accept': 'application/json'}, timeout=(10, 20))
            if existing.status_code == 404:
                res = existing
            else:
                res = None
            if res is None:
                assert existing.status_code == 200, 'Cannot verify cleanup ownership'
                assert existing.json().get('firstname') == payload['firstname'], 'ID ownership changed; refusing deletion'
                res = api.session.request('DELETE', api.base_url + f'/booking/{bid}',
                cookies={'token': token}, timeout=(10, 20))
        except Exception as exc:
            pytest.fail(f'Cleanup failed for test-owned booking {bid}: {type(exc).__name__}')
        assert res.status_code in (201, 404), f'Cleanup failed: id={bid}, status={res.status_code}'


def pytest_configure(config):
    config._case_results = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    rows = item.config._case_results
    row = rows.setdefault(item.nodeid, {'nodeid': item.nodeid,
        'kind': 'live' if 'live' in item.keywords else 'offline', 'phases': {}, 'requests': []})
    row['phases'][report.when] = report.outcome
    row['requests'] = list(getattr(item, '_api_trace', []))
    # Failure details remain in pytest/JUnit; structured traces never copy request payloads/tokens.


def pytest_sessionfinish(session, exitstatus):
    output = os.getenv('BOOKING_CASE_RESULTS')
    if output:
        Path(output).write_text(json.dumps({'exit_code': int(exitstatus),
            'cases': list(session.config._case_results.values())},
            ensure_ascii=False, indent=2), encoding='utf-8')
