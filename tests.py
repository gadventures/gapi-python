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

if __name__ == '__main__':
    unittest.main()
