import pytest
from booking.checks import check_booking
pytestmark = [pytest.mark.live, pytest.mark.write]

def test_create_read_roundtrip(api, owned):
    bid, payload, result = owned
    assert result.get('booking') == payload
    actual = api.json('GET', f'/booking/{bid}', 200)
    check_booking(actual)
    assert actual == payload

def test_full_update(api, token, owned):
    bid, payload, _ = owned
    updated = {**payload, 'lastname': 'Updated', 'totalprice': 456, 'depositpaid': False}
    assert api.json('PUT', f'/booking/{bid}', 200, json=updated, cookies={'token': token}) == updated
    assert api.json('GET', f'/booking/{bid}', 200) == updated

def test_partial_update(api, token, owned):
    bid, payload, _ = owned
    change = {'additionalneeds': 'Late check-in'}
    assert api.json('PATCH', f'/booking/{bid}', 200, json=change, cookies={'token': token}) == {**payload, **change}
    assert api.json('GET', f'/booking/{bid}', 200) == {**payload, **change}

def test_unauthorized_update_preserves_data(api, owned):
    bid, payload, _ = owned
    api.call('PUT', f'/booking/{bid}', 403, json={**payload, 'totalprice': 999})
    assert api.json('GET', f'/booking/{bid}', 200) == payload

def test_delete_then_not_found(api, token, owned):
    bid, _, _ = owned
    api.call('DELETE', f'/booking/{bid}', 201, cookies={'token': token})
    api.call('GET', f'/booking/{bid}', 404)
