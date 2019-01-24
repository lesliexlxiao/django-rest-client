
# -*- coding: utf-8 -*-
import logging
import json
import urlparse

import requests
from requests.exceptions import RequestException

from django_rest_client.exceptions import ConfigError, ServerResponseError, \
    InvalidRestMethodError, DebugError, RestClientError
from django_rest_client.models import DjangoRestClient
from django_rest_client.decorators import json_format
from django_rest_client.settings import REST_CLIENT_SETTINGS

logger = logging.getLogger('django_rest_client')

ALLOWED_HTTP_METHODS = frozenset(('GET', 'POST', 'PUT', 'DELETE', 'PATCH'))


class Client(object):
    _parser = staticmethod(json.loads)
    _error_parser = staticmethod(lambda x: x)
    _config_name = None
    _default_profile = 'default'
    _base_url_path = ''
    _default_timeout = 3
    _exception_class = None

    def __init__(self, profile):
        self._config = {}
        self._base_url = None
        self._timeout = self._default_timeout
        self.profile = profile
        self.load_config()

    def load_config(self):
        class_name = self.__class__.__name__

        if self._config_name is None:
            raise ConfigError('Please set "_config_name" for setting lookup')

        rest_client_config = DjangoRestClient.objects.filter(name=self._config_name).first() \
            or REST_CLIENT_SETTINGS.get(self._config_name, {})

        if not rest_client_config:
            raise ConfigError('Config name for {} class_name is not found.'
                              .format(self._config_name))

        if self.profile and self.profile in rest_client_config:
            self._config = rest_client_config[self.profile]
        else:
            raise ConfigError('Configuration for {} is not found with profile {}'
                              .format(class_name, self.profile))

        self._config['config_profile'] = self.profile
        self._config['_class'] = class_name

        self._base_url = self._build_base_url()
        self._timeout = self._config.get('TIMEOUT', self._default_timeout)

    def _build_base_url(self):
        scheme = self._config.get('SCHEMreE', 'http')
        hostname = self._config['HOSTNAME']
        port = self._config.get('PORT', 80)
        base_url = '{}://{}:{}'.format(scheme, hostname, port)

        if not self._base_url_path:
            base_url = urlparse.urljoin(base_url, self._base_url_path)

        return base_url

    def _concat_url(self, url):
        return '{}/{}'.format(self._base_url, url)

    def _rest_call(self, url, method='GET', **kwargs):
        def generate_exc_data(response):
            return {'url': url, 'response': response, 'kwargs': kwargs, 'client': self}

        encoding = kwargs.pop('encoding', None)
        debug = kwargs.pop('debug', False)
        discard_error = kwargs.pop('discard_error', False)

        url = self._concat_url(url)

        if method in ALLOWED_HTTP_METHODS:
            try:
                kwargs.setdefault('timeout', self._timeout)
                response = requests.request(method.lower(), url, verify=True, **kwargs)
            except RequestException as e:
                response = requests.Response()  # fake a response to facilitate error handle
                response._content = 'Connection error {}'.format(e.message)
                raise ServerResponseError(**generate_exc_data(response))

            if debug:
                raise DebugError(**generate_exc_data(response))
        else:
            raise InvalidRestMethodError(
                'Invalid method "{}" is used for the HTTP request. Can only'
                'use the following: {!s}'.format(method, ALLOWED_HTTP_METHODS)
            )

        if 200 <= response.status_code < 300:
            if encoding is not None:
                response.encoding = encoding
            response_data = response.text.strip()
            return self._parser(response_data) if response_data else None
        else:
            exc = ServerResponseError(**generate_exc_data(response))

            if not discard_error:
                logger.error(exc.message)
            self._error_handler(exc)

    def _error_handler(self, exception):
        raise exception


class JSONClient(Client):

    def __init__(self, profile, *args, **kwargs):
        super(JSONClient, self).__init__(profile, *args, **kwargs)
        self._mapping = kwargs.get('mapping', {})

    @json_format
    def _rest_call(self, url, method, **kwargs):

        try:
            rsp = super(JSONClient, self)._rest_call(url, method, **kwargs)
        except RestClientError as e:
            raise e
        else:
            return rsp


class RestClientFactory(object):
    _instances = {}

    @classmethod
    def client_class(cls, profile):
        raise NotImplementedError('No client can be used for {} profile in {}'
                                  .format(profile, cls.__name__))

    def __new__(cls, profile='default', *args, **kwargs):
        # Ensure profile as lowercase
        profile = profile.lower()

        try:
            client = cls._instances[profile]
        except KeyError:
            _class = cls.client_class(profile)
            client = cls._instances[profile] = _class(profile, *args, **kwargs)

        return client
