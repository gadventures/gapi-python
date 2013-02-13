import requests
import json

API_ROOT = 'http://rest.gadventures.com'
APPLICATION_KEY = ''

class ApiBase(object):
    def _request(self, uri, method, data=None):
        """
        Make an HTTP request to a target API method with proper headers.
        """
        assert method in ['GET', 'POST', 'PUT'], "Only 'GET', 'POST', and 'PUT' are allowed."

        url = API_ROOT + uri

        headers = {'Content-Type': 'application/json', 'X-Application-Key': APPLICATION_KEY}

        requests_call = getattr(requests, method.lower())
        request = requests_call(url, headers=headers, data=data)

        response_dict = json.loads(request.text)

        return response_dict

class ApiObject(ApiBase):
    def __init__(self, resource_name, data_dict=None):
        self._resource_name = resource_name
        self._object_id = None
        self._updated_at = None

        self._data_dict = {}
        if data_dict:
            self._populate_from_dict(data_dict)

    def _populate_from_dict(self, data_dict):
        if 'id' in data_dict:
            self._object_id = data_dict['id']

        if 'updated_at' in data_dict:
            self._updated_at = data_dict['updated_at']
        self._data_dict.update(data_dict)

    def save(self):
        if self._object_id:
            self._update()
        else:
            self._create()

    def as_dict(self):
        properties = [(k, v) for k, v in self._data_dict.items()
                        if not k.startswith('_')]
        return dict(properties)
        
    def as_json(self):
        return json.dumps(self.as_dict())

    def _update(self):
        uri = '/{0}/{1}/'.format(self._resource_name, self._object_id)
        data = self.as_json()
        response_dict = self._request(uri, 'PUT', data)

    def _create(self):
        uri = '/{0}/'.format(self._resource_name)
        data = self.as_json()
        response_dict = self._request(uri, 'POST', data)
        self._object_id = response_dict['id']

    def __repr__(self):
        return '<{}: {}>'.format(self._resource_name, self._object_id)

class Query(ApiBase):
    def __init__(self, resource_name):
        self._resource_name = resource_name
        self._object_id = None
        self._parent = None

    def get(self, object_id):
        self._object_id = object_id
        return self._fetch(single_result=True)

    def parent(self, resource_name, resource_id):
        self._parent = (resource_name, resource_id)
        return self

    def fetch(self):
        return self._fetch()

    def _fetch(self, single_result=False):
        if self._object_id:
            uri = '/{0}/{1}/'.format(self._resource_name, self._object_id)
        else:
            if self._parent:
                uri = '/{1}/{2}/{0}/'.format(self._resource_name, *self._parent)
            else:
                uri = '/{0}/'.format(self._resource_name)

        response_dict = self._request(uri, 'GET')

        if single_result:
            return ApiObject(self._resource_name, response_dict)
        else:
            return [ApiObject(self._resource_name, result) for
                        result in response_dict['results']]
