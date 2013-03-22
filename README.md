gapi-python is a Python client for the G Adventures REST API. It provides Python
object mapping for methods to save, update and delete objects, as well as an
interface for querying stored objects.

Usage
===

You'll need to provide your G-API _Application Key_. This is available from your
G-API Dashboard

    >>> import gapipy as gapi
    >>> gapi.APPLICATION_KEY = 'your application_key'

Query for a list of resources:

    >>> query = gapi.Query('customers')
    >>> query.fetch()

Get a single resource:

    >>> gapi.Query('customers').get('xxAaBceD')

Query a list of resources via a parent criteria. This takes advantage of a
helpful feature in the API which makes it easy to query for related resources.

    >>> gapi.Query('bookings').parent('customers', 'xxAaBceD').fetch()

Update a fetched resource, sending the full resource (PUT):

    >>> customer = gapi.Query('customers').get('xxAaBceD')
    >>> customer.set({'first_name': 'Bubot'})
    >>> customer.save()

Update a fetched resource, with only data that has been changed (PATCH)

    >>> customer = gapi.Query('customers').get('xxAaBceD')
    >>> customer.set({'emergency_contact': '555-555-5555'})
    >>> customer.save(partial=True)

Filtering Resources
===

You are able to filter resources based on some simple operators.

For instance, simple equality checks:

    >>> gapi.Query('customers').eq('last_name', 'Bronson')
    >>> gapi.Query('customers').eq('first_name', 'Action').eq('last_name', 'Bronson')

Advanced Usage
====

Although it will be very rare that you change `API_ROOT`, unless you're hosting
your own API layer, it can be common for you to adjust `API_PROXY`. By changing
this variable, all links returned by the API will be relative to `API_PROXY`

Dependencies
===

* [requests](http://docs.python-requests.org/en/latest/)
