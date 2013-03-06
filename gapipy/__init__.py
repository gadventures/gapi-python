import requests
import json

API_ROOT = 'http://rest.gadventures.com'
APPLICATION_KEY = ''

class ApiBase(object):
    def _request(self, uri, method, data=None):
        """
        Make an HTTP request to a target API method with proper headers.
        """
        assert method in ['GET', 'POST', 'PUT', 'PATCH'], "Only 'GET', 'POST', 'PUT', and 'PATCH' are allowed."

        url = API_ROOT + uri

        headers = {'Content-Type': 'application/json', 'X-Application-Key': APPLICATION_KEY}

        requests_call = getattr(requests, method.lower())

        request = requests_call(url, headers=headers, data=data)

        if request.status_code in (requests.codes.ok, requests.codes.created,
                requests.codes.accepted):
            response_dict = json.loads(request.text)
            return response_dict
        else:
            request.reason = request.text
            return request.raise_for_status()

class ApiObject(ApiBase):
    def __init__(self, resource_name, data_dict=None):
        self._resource_name = resource_name
        self._object_id = None
        self._updated_at = None

        self._changed = []
        self._data_dict = {}
        if data_dict:
            self._populate_from_dict(data_dict)

    def set(self, data_dict):
        self._changed.extend(data_dict.keys())
        self._data_dict.update(data_dict)

    def _populate_from_dict(self, data_dict):
        if 'id' in data_dict:
            self._object_id = data_dict['id']

        if 'updated_at' in data_dict:
            self._updated_at = data_dict['updated_at']

        self._data_dict.update(data_dict)

    def save(self, partial=False):
        if self._object_id:
            self._update(partial=partial)
        else:
            self._create()
        self._changed = []

    def as_dict(self, partial=False):
        update_fields = self._data_dict.keys()
        if partial:
            update_fields = self._changed

        properties = [(k, v) for k, v in self._data_dict.items()
                        if not k.startswith('_') and k in update_fields]
        return dict(properties)
        
    def as_json(self, partial=False):
        return json.dumps(self.as_dict(partial=partial))

    def _update(self, partial=False):
        method = 'PATCH' if partial else 'PUT'

        uri = '/{0}/{1}/'.format(self._resource_name, self._object_id)
        data = self.as_json(partial=partial)
        response_dict = self._request(uri, method, data)

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
