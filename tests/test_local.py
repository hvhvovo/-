from unittest.mock import Mock
import pytest
import requests
from booking.client import Client, ApiError
from booking.checks import check_booking

def sample():
    return {'firstname': 'QA', 'lastname': 'Test', 'totalprice': 100, 'depositpaid': False,
        'bookingdates': {'checkin': '2027-05-10', 'checkout': '2027-05-12'}}

def test_valid_contract():
    check_booking(sample())

@pytest.mark.parametrize('field,bad', [('firstname', 1), ('lastname', None),
    ('totalprice', True), ('totalprice', '100'), ('depositpaid', 1), ('bookingdates', [])])
def test_invalid_field_types(field, bad):
    value = sample(); value[field] = bad
    with pytest.raises(AssertionError): check_booking(value)

@pytest.mark.parametrize('value', ['2027-02-30', '2027/05/10', 'invalid', 123])
def test_invalid_dates(value):
    data = sample(); data['bookingdates']['checkin'] = value
    with pytest.raises((AssertionError, ValueError)): check_booking(data)

def test_network_failure_is_distinguishable():
    session = Mock(); session.request.side_effect = requests.Timeout('example')
    with pytest.raises(ApiError, match='network failure'):
        Client('https://example.test', session).call('GET', '/booking', 200)
    assert session.request.call_count == 1

def test_wrong_status_diagnostic():
    session = Mock(); session.request.return_value.status_code = 503
    session.request.return_value.text = 'Unavailable'
    with pytest.raises(AssertionError, match='expected 200, got 503'):
        Client('https://example.test', session).call('GET', '/booking', 200)

def test_invalid_json_diagnostic():
    session = Mock(); res = session.request.return_value; res.status_code = 200
    res.json.side_effect = ValueError(); res.text = 'not-json'
    with pytest.raises(ApiError, match='Invalid JSON'):
        Client('https://example.test', session).json('GET', '/booking', 200)

@pytest.mark.parametrize('cleanup_case', ['present', 'missing', 'changed_owner'])
def test_cleanup_checks_ownership(cleanup_case):
    from conftest import owned
    api = Mock(); api.base_url = 'https://example.test'
    api.json.return_value = {'bookingid': 77}
    flow = owned.__wrapped__(api, 'demo-token')
    bid, payload, _ = next(flow)
    existing = Mock()
    existing.status_code = 404 if cleanup_case == 'missing' else 200
    existing.json.return_value = {'firstname': 'other' if cleanup_case == 'changed_owner' else payload['firstname']}
    deleted = Mock(); deleted.status_code = 201
    api.session.request.side_effect = [existing, deleted]
    if cleanup_case == 'changed_owner':
        with pytest.raises(pytest.fail.Exception, match='Cleanup failed'):
            next(flow)
    else:
        with pytest.raises(StopIteration): next(flow)
    methods = [c.args[0] for c in api.session.request.call_args_list]
    assert methods == (['GET', 'DELETE'] if cleanup_case == 'present' else ['GET'])
