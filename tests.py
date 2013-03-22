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

    def test_modify_attribute(self):
        obj = gapi.ApiObject('customers', {
            'first_name': 'Florence',
            'last_name': 'Machine',
        })

        obj.set({'first_name': 'The'})

        self.assertEquals(obj.as_dict(), {'first_name': 'The', 'last_name': 'Machine'})

    def test_watch_modified(self):
        obj = gapi.ApiObject('customers', {
            'id': 100,
            'first_name': 'Florence',
            'last_name': 'Machine',
        })
        obj.set({'first_name': 'Portis', 'last_name': 'head'})
        self.assertEquals(obj.as_dict(), {'first_name': 'Portis', 'id': 100, 'last_name': 'head'})
        self.assertEquals(obj._changed, ['first_name', 'last_name'])

        # Upon saving the object, changed should be cleared.
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            obj.save(partial=True)
            mock_request.assert_called_with(
                '/customers/100/',
                'PATCH',
                '{"first_name": "Portis", "last_name": "head"}',
            )

        self.assertEquals(obj._changed, [])

    def test_update_put(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request, \
             mock.patch('gapipy.Query._fetch_one') as mock_fetch:
            mock_fetch.return_value = gapi.ApiObject('customers', {
                'id': '00130000011iW14AAE',
                'name': 'Action',
            })
            obj = gapi.Query('customers').get('00130000011iW14AAE')

            obj.save()
            mock_request.assert_called_with(
                '/customers/00130000011iW14AAE/',
                'PUT',
                '{"id": "00130000011iW14AAE", "name": "Action"}'
            )

    def test_where_eq(self):
        with mock.patch('gapipy.ApiBase._request') as mock_request:
            mock_request.return_value = {
                'results': [{
                'id': '1',
                'name': 'Bronson',
                }]
            }
            query = gapi.Query('customers').eq('email', 'channel@orange.com')

            # Query is lazy, not called until we evaluate it.
            results = list(query.fetch())

            mock_request.assert_called_with(
                '/customers/',
                'GET',
                options={'where': '{"email": "channel@orange.com"}'},
            )

if __name__ == '__main__':
    unittest.main()
