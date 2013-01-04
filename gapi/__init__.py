import urllib2
import json

API_ROOT = 'http://rest.gadventures.com'
APPLICATION_KEY = ''

class ApiBase(object):
    def _request(self, uri, method):
        """
        Make an HTTP request to a target API method with proper headers.
        """
        assert method in ['GET','POST', 'PUT'], "Only 'GET', 'POST', and 'PUT' are allowed."

        url = API_ROOT + uri

        print "Hitting url", url

        request = urllib2.Request(url)
        request.add_header('Content-Type', 'application/json')

        request.add_header('X-Application-Key', APPLICATION_KEY)

        request.get_method = lambda: method

        response = urllib2.urlopen(request)
        response_body = response.read()
        response_dict = json.loads(response_body)
        return response_dict

class ApiObject(ApiBase):
    def __init__(self, resource_name, data_dict=None):
        self._resource_name = resource_name

        # sloppy but simple for now.
        if data_dict:
            self.__dict__.update(data_dict)

    def __repr__(self):
        return '<{}: {}>'.format(self._resource_name, getattr(self, 'id', None))

class Query(ApiBase):
    def __init__(self, resource_name):
        self._resource_name = resource_name
        self._object_id = None

    def get(self, object_id):
        self._object_id = object_id
        return self._fetch(single_result=True)

    def fetch(self):
        return self._fetch()

    def _fetch(self, single_result=False):
        if self._object_id:
            uri = '/{0}/{1}/'.format(self._resource_name, self._object_id)
        else:
            uri = '/{0}/'.format(self._resource_name)

        response_dict = self._request(uri, 'GET')

        if single_result:
            return ApiObject(self._resource_name, response_dict)
        else:
            return [ApiObject(self._resource_name, result) for
                        result in response_dict['results']]

        return self._fetch()
