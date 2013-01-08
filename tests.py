import unittest
import mock

import gapi

gapi.APPLICATION_KEY = 'FAKE'

class ApiTestCase(unittest.TestCase):
    """
    Not a working test case."
    """
    def test_query(self):
        query = gapi.Query('customers')
        results = query.fetch()

    def test_get(self):
        result = gapi.Query('customers').get('00130000011iW14AAE')

    def test_update(self):
        with mock.patch('gapi.ApiBase._request') as mock_request, \
             mock.patch('gapi.Query._fetch') as mock_fetch:
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
