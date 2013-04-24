import json
import unittest
import mock

import gapipy as gapi

gapi.REST_API_ROOT = 'http://127.0.0.1'
gapi.APPLICATION_KEY = 'TESTER'

class ApiTestCase(unittest.TestCase):
    def test_query(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            mock_request.return_value = {
                'results': [{
                'id': '1',
                'name': 'Bronson',
                }]
            }

            query = gapi.Query('customers')
            results = query.fetch()
            self.assertEquals([json.loads(r.as_json()) for r in results],
                    [{"id": "1", "name": "Bronson"}])

    def test_query_with_parent(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            mock_request.return_value = {
                'results': [{
                    'id': '1',
                    'name': 'Emperor',
                }]
            }
            query = gapi.Query('bookings').parent('customers', '1')

            results = query.fetch()
            self.assertEquals([r.as_dict() for r in results],
                    [{'id': '1', 'name': 'Emperor'}])

    def test_get(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            mock_request.return_value = {
                    'id': '1',
                    'name': 'Carmack',
            }
            result = gapi.Query('customers').get('1')

            self.assertEquals(json.loads(result.as_json()),
                    {'id': '1', 'name': 'Carmack'})

    def test_where_eq(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            query = gapi.Query('customers').eq('email', 'channel@orange.com')

            # Query is lazy, not called until we evaluate it.
            results = list(query.fetch())

            mock_request.assert_called_with(
                '/customers',
                'GET',
                options={"email": "channel@orange.com"},
            )

if __name__ == '__main__':
    unittest.main()
