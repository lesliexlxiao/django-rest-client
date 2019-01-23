Django Rest Client
==================

Rest Client aimed to be a python utility kit for all rest services.


Requirements
------------

- Python (2.7, 3.2, 3.3, 3.4, 3.5)
- Django (1.8, 1.9, 1.10)
- `jsonfield (2.0.2) <https://github.com/dmkoch/django-jsonfield>`_
- `django-jsoneditor (0.0.2) <https://github.com/nnseva/django-jsoneditor>`_
- requests (2.18.4)


Installation
------------

Install using pip:

.. code-block:: sh

    pip install django-rest-client


Configuration
-------------

Add ``'django_rest_client'`` to your ``INSTALLED_APPS`` of your `settings.py` file.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_rest_client',
    ]


Usage
-----