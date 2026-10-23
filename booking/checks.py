from datetime import date

def check_booking(data):
    assert isinstance(data, dict), 'Booking must be an object'
    for field, kind in [('firstname', str), ('lastname', str), ('totalprice', int),
                        ('depositpaid', bool), ('bookingdates', dict)]:
        assert field in data, f'Missing field: {field}'
        assert type(data[field]) is kind, f'Wrong type: {field}'
    for field in ['checkin', 'checkout']:
        assert field in data['bookingdates'], f'Missing date: {field}'
        value = data['bookingdates'][field]
        assert isinstance(value, str), f'Date must be text: {field}'
        assert date.fromisoformat(value).isoformat() == value
