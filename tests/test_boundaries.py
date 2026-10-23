"""Contract-based checks on test-owned records; no pressure/load tests."""
import pytest
from booking.checks import check_booking
pytestmark = [pytest.mark.live, pytest.mark.write]

@pytest.mark.parametrize('method,use_bad_token', [('PATCH', False), ('DELETE', False), ('PUT', True)])
def test_denied_write_preserves_record(api, owned, method, use_bad_token):
    bid, payload, _ = owned
    kwargs = {'cookies': {'token': 'qa-invalid-token'}} if use_bad_token else {}
    if method == 'PUT': kwargs['json'] = {**payload, 'totalprice': 999}
    if method == 'PATCH': kwargs['json'] = {'totalprice': 999}
    api.call(method, f'/booking/{bid}', 403, **kwargs)
    assert api.json('GET', f'/booking/{bid}', 200) == payload

@pytest.mark.parametrize('fields', [('firstname',), ('firstname', 'lastname')])
def test_filter_contains_created_booking(api, owned, fields):
    bid, payload, _ = owned
    params = {field: payload[field] for field in fields}
    rows = api.json('GET', '/booking', 200, params=params)
    assert isinstance(rows, list)
    ids = []
    for row in rows:
        assert isinstance(row, dict) and type(row.get('bookingid')) is int
        ids.append(row['bookingid'])
    assert bid in ids, f'Created booking {bid} missing from filtered results'
    # Random firstname is unique in this run; no claim about global exact result count.

@pytest.mark.parametrize('field,value', [('totalprice', 0), ('depositpaid', False), ('additionalneeds', '')])
def test_valid_boundary_values_persist(api, owned, token, field, value):
    bid, payload, _ = owned
    updated = {**payload, field: value}
    response = api.json('PUT', f'/booking/{bid}', 200, json=updated, cookies={'token': token})
    check_booking(response)
    assert response == updated
    assert api.json('GET', f'/booking/{bid}', 200) == updated
