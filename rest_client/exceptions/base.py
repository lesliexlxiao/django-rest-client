from django_rest_client.utils import Guardor


class RestClientError(Exception):

    @property
    def err_msg(self):
        return str(self)


class ConfigError(RestClientError):
    pass


class InvalidRestMethodError(RestClientError):
    pass


class ServerResponseError(RestClientError):
    """Server response error class for client."""

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], ServerResponseError):
            self._kwargs = args[0].kwargs
            self.url = args[0].url
            self.response = args[0].response
            self.client = args[0].client
        else:
            self._kwargs = kwargs.pop('kwargs', None)
            self.url = kwargs.pop('url', None)
            self.response = kwargs.pop('response', None)
            self.client = kwargs.pop('client', None)
        super(ServerResponseError, self).__init__(*args, **kwargs)

    def __str__(self):
        if self.response is not None:
            rsp = self.response

            if rsp is not None:
                body = self.client._error_parser(rsp.text)

                msg = (u'{0.url} returned HTTP {1.status_code}: {0.kwargs}'
                       u'Response Headers: {1.headers} Body: {2}').format(
                           self, rsp, body)
            else:
                msg = (u'{0.url} error: {1.kwargs}').format(self)
            return u'Server response not OK. Verbose: {}'.format(msg)
        else:
            return super(ServerResponseError, self).__str__()

    @property
    def kwargs(self):
        return Guardor.cleanse_content(self._kwargs)

    @property
    def err_msg(self):
        if self.response._content:
            try:
                return self.response.json()
            except:
                return self.response.text
        else:
            return str(self)

    @property
    def message(self):
        return str(self)

    def __repr__(self):
        result = super(ServerResponseError, self).__repr__()
        detail_info = u'ServerResponseException({}),'.format(repr(self.message))
        return result.replace(u'ServerResponseException(),', detail_info)


class DebugError(ServerResponseError):

    def __str__(self):
        if self.response is not None:
            rsp = self.response

            if rsp is not None:
                body = self.client._error_parser(rsp.text)

                msg = (u'{0.url} returned HTTP {1.status_code}: {0.kwargs}\n'
                       u'Response Headers: {1.headers} \nBody: {2}').format(
                           self, rsp, body)
            else:
                msg = (u'{0.url} error: {1.kwargs}').format(self)
            return u'Debug Details: \n{}'.format(msg)
        else:
            return super(ServerResponseError, self).__str__()
