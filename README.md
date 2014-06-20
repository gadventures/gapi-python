# DEPRECATED IN FAVOUR OF `gapipy`
## https://github.com/gadventures/gapipy

gapi-python is a simple Python client for the G Adventures API. It provides Python
object mapping for methods to save, update and delete objects, as well as an
interface for querying stored objects.

Usage
===

You'll need to provide your G Adventures API _Application Key_. This is
available from your G Adventures API Dashboard

    >>> import gapipy as gapi
    >>> gapi.APPLICATION_KEY = 'your application_key'

Query for a list of resources:

    >>> query = gapi.Query('tours')
    >>> query.fetch()

Get a single resource:

    >>> gapi.Query('tours').get(9649)

Query a list of resources via a parent criteria. This takes advantage of a
helpful feature in the API which makes it easy to query for related resources.

    >>> gapi.Query('departures').parent('tours', 9649).fetch()

Saving Objects
===

Currently, as the G Adventures API only supports reading, there is no notion of
updating and creating within this client.

Filtering Resources
===

You are able to filter resources based on some simple operators.

For instance, simple equality checks:

    >>> gapi.Query('dossiers').eq('dossier_code', 'PPP')

Chaining is of course, allowed for multiple equality checks..

Advanced Usage
====

Although it will be very rare that you change `API_ROOT`, unless you're hosting
your own API layer, it can be common for you to adjust `API_PROXY`. By changing
this variable, all links returned by the API will be relative to `API_PROXY`


Dependencies
===

* [requests](http://docs.python-requests.org/en/latest/)

Develop
===

Run tests:

    pip install nose mock
    nosetests

Then work your magic!
