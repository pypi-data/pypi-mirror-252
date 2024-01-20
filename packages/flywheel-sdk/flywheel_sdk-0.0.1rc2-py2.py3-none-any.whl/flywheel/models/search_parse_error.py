# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401
import six

class SearchParseError(object):

    swagger_types = {
        'line': 'int',
        'pos': 'int',
        'offset': 'int',
        'message': 'str'
    }

    attribute_map = {
        'line': 'line',
        'pos': 'pos',
        'offset': 'offset',
        'message': 'message'
    }

    rattribute_map = {
        'line': 'line',
        'pos': 'pos',
        'offset': 'offset',
        'message': 'message'
    }

    def __init__(self, line=None, pos=None, offset=None, message=None):  # noqa: E501
        """SearchParseError - a model defined in Swagger"""
        super(SearchParseError, self).__init__()

        self._line = None
        self._pos = None
        self._offset = None
        self._message = None
        self.discriminator = None
        self.alt_discriminator = None

        if line is not None:
            self.line = line
        if pos is not None:
            self.pos = pos
        if offset is not None:
            self.offset = offset
        self.message = message

    @property
    def line(self):
        """Gets the line of this SearchParseError.

        The line number where the error occurred

        :return: The line of this SearchParseError.
        :rtype: int
        """
        return self._line

    @line.setter
    def line(self, line):
        """Sets the line of this SearchParseError.

        The line number where the error occurred

        :param line: The line of this SearchParseError.  # noqa: E501
        :type: int
        """

        self._line = line

    @property
    def pos(self):
        """Gets the pos of this SearchParseError.

        The position where the error occurred

        :return: The pos of this SearchParseError.
        :rtype: int
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        """Sets the pos of this SearchParseError.

        The position where the error occurred

        :param pos: The pos of this SearchParseError.  # noqa: E501
        :type: int
        """

        self._pos = pos

    @property
    def offset(self):
        """Gets the offset of this SearchParseError.

        The absolute offset in the input (from 0) where the error occurred

        :return: The offset of this SearchParseError.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this SearchParseError.

        The absolute offset in the input (from 0) where the error occurred

        :param offset: The offset of this SearchParseError.  # noqa: E501
        :type: int
        """

        self._offset = offset

    @property
    def message(self):
        """Gets the message of this SearchParseError.

        The error message

        :return: The message of this SearchParseError.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this SearchParseError.

        The error message

        :param message: The message of this SearchParseError.  # noqa: E501
        :type: str
        """

        self._message = message


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SearchParseError):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
