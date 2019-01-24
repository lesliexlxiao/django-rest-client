from django.utils.functional import SimpleLazyObject


class Client(object):
    pass


class ClientFactory(object):

    def __new__(cls, profile='default', **kwargs):
        if '_instances' not in cls.__dict__:
            setattr(cls, '_instances', {})

        profile = profile.lower()

        try:
            client = cls._instances[profile]
        except KeyError:
            _class = cls.client_class(profile)
            client = cls._instances[profile] = SimpleLazyObject(lambda: _class(profile, **kwargs))
        return client

    @classmethod
    def client_class(cls, profile):
        raise NotImplementedError('No client can be used for {} profile in {}'
                                  .format(profile, cls.__name__))
