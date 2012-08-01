import os

__version__ = '0.1.2'


class Environment(object):

    def __init__(self, prefix=None):
        self.prefix = prefix
        self.environ = os.environ

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.environ)

    def get(self, key, default=None):
        if self.prefix is not None:
            key = '{0}_{1}'.format(self.prefix, key)

        return self.environ.get(key, default)

    def bool(self, key, default=None):
        """
        Returns a boolean if you pass in a truthy or falsy value.

        Valid truth values are::
            1, '1', 'true', 't', 'True' and 'TRUE'

        Valid falsey valus are::
            0, '0', 'false', 'f', 'False' and 'FALSE'

        If the value is not truthy or falsey this will raise a
        value error.

        """
        value = self.get(key, default)

        if value in (True, False):
            return bool(value)

        if value in ('1', 'true', 't', 'True', 'TRUE'):
            return True

        if value in ('0', 'false', 'f', 'False', 'FALSE'):
            return False

        raise ValueError("invalid value for bool(): '{0}'".format(value))

    def int(self, key, default=None):
        """
        Returns the found value converted to a integer.

        """
        return int(self.get(key, default))

    def list(self, key, default=None, corce=lambda x: x):
        """
        Returns the found value converted to a list. You can
        also pass a corce callable to change the datatype.

        """
        value = self.get(key, default)

        if isinstance(value, (list, tuple)):
            return value

        return [corce(i.strip()) for i in value.split(',')]
