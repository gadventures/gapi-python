import json
import unittest
import mock

import gapipy as gapi

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
            query = gapi.Query('bookings').parent('customers', 'aaBBceDz')

            results = query.fetch()
            self.assertEquals([r.as_dict() for r in results],
                    [{'id': '1', 'name': 'Emperor'}])

    def test_get(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            mock_request.return_value = {
                    'id': '1',
                    'name': 'Carmack',
            }
            result = gapi.Query('customers').get('00130000011iW14AAE')

            self.assertEquals(json.loads(result.as_json()),
                    {'id': '1', 'name': 'Carmack'})

    def test_update(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request, \
             mock.patch('gapipy.Query._fetch') as mock_fetch:
            mock_fetch.return_value = gapi.ApiObject('customers', {
                'id': '1',
                'name': 'Action',
            })
            obj = gapi.Query('customers').get('00130000011iW14AAE')

            obj.save()
            self.assertTrue(mock_request.called_with(
                'http://rest.gadventures.com/customers/00130000011iW14AAE/',
                'PUT',
                '{"name": "Action"}'
            ))

if __name__ == '__main__':
    unittest.main()
