gapi-python is a Python client for the G Adventures REST API. It provides Python
object mapping for methods to save, update and delete objects, as well as an
interface for querying stored objects.

Usage
===

You'll need to provide your G-API _Application Key_. This is available from your
G-API Dashboard

    >>> import gapi
    >>> gapi.APPLICATION_KEY = 'your application_key'

Query for a list of resources:

    >>> query = gapi.Query('customers')
    >>> query.fetch()

Get a single resource:

    >>> gapi.Query('customers').get('xxAaBceD')

Update a fetched resource:

    >>> customer = gapi.Query('customers').get('xxAaBceD')
    >>> # do things to customer data.
    >>> customer.save()

Dependencies
===

* [requests](http://docs.python-requests.org/en/latest/)
