import pytest
from booking.checks import check_booking
pytestmark = pytest.mark.live

def test_list_contract(api):
    rows = api.json('GET', '/booking', 200)
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        assert type(row.get('bookingid')) is int

def test_detail_contract(api):
    rows = api.json('GET', '/booking', 200)
    assert isinstance(rows, list)
    if not rows:
        pytest.skip('Shared environment contains no bookings')
    assert isinstance(rows[0], dict) and type(rows[0].get('bookingid')) is int
    check_booking(api.json('GET', f"/booking/{rows[0]['bookingid']}", 200))

def test_unknown_route(api):
    api.call('GET', '/qa-route-that-does-not-exist', 404)

def test_invalid_credentials(api):
    body = api.json('POST', '/auth', 200,
        json={'username': 'qa_invalid_user', 'password': 'invalid_password'})
    assert isinstance(body, dict) and not body.get('token')
    assert body.get('reason') == 'Bad credentials'
