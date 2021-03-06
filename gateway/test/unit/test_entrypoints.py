import json
import pytest
from marshmallow import ValidationError
from gateway.entrypoints import HttpEntrypoint

class TestHttpEntrypoint(object):

    @pytest.mark.parametrize(
        ('exc', 'expected_error', 'expected_status_code',
            'expected_message'), [
            (ValueError('unexpected'), 'UNEXPECTED_ERROR', 500, 'unexpected'),
            (ValidationError('v1'), 'VALIDATION_ERROR', 400, 'v1'),
            (TypeError('t1'), 'BAD_REQUEST', 400, 't1'),
        ]
    )
    def test_error_handling(
        self, exc, expected_error, expected_status_code, expected_message
    ):
        entrypoint = HttpEntrypoint('GET', 'url')
        entrypoint.expected_exceptions = (
            ValidationError,
            TypeError,
        )

        response = entrypoint.response_from_exception(exc)
        response_data = json.loads(response.data.decode())

        assert response.mimetype == 'application/json'
        assert response.status_code == expected_status_code
        assert response_data['error'] == expected_error
        assert response_data['message'] == expected_message
