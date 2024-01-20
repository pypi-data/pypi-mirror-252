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

class FileSuggestion(object):

    swagger_types = {
        'name': 'str',
        'file_id': 'str',
        'version': 'int',
        'suggested': 'dict(str, bool)'
    }

    attribute_map = {
        'name': 'name',
        'file_id': 'file_id',
        'version': 'version',
        'suggested': 'suggested'
    }

    rattribute_map = {
        'name': 'name',
        'file_id': 'file_id',
        'version': 'version',
        'suggested': 'suggested'
    }

    def __init__(self, name=None, file_id=None, version=None, suggested=None):  # noqa: E501
        """FileSuggestion - a model defined in Swagger"""
        super(FileSuggestion, self).__init__()

        self._name = None
        self._file_id = None
        self._version = None
        self._suggested = None
        self.discriminator = None
        self.alt_discriminator = None

        self.name = name
        self.file_id = file_id
        self.version = version
        self.suggested = suggested

    @property
    def name(self):
        """Gets the name of this FileSuggestion.


        :return: The name of this FileSuggestion.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FileSuggestion.


        :param name: The name of this FileSuggestion.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def file_id(self):
        """Gets the file_id of this FileSuggestion.


        :return: The file_id of this FileSuggestion.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id):
        """Sets the file_id of this FileSuggestion.


        :param file_id: The file_id of this FileSuggestion.  # noqa: E501
        :type: str
        """

        self._file_id = file_id

    @property
    def version(self):
        """Gets the version of this FileSuggestion.


        :return: The version of this FileSuggestion.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this FileSuggestion.


        :param version: The version of this FileSuggestion.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def suggested(self):
        """Gets the suggested of this FileSuggestion.


        :return: The suggested of this FileSuggestion.
        :rtype: dict(str, bool)
        """
        return self._suggested

    @suggested.setter
    def suggested(self, suggested):
        """Sets the suggested of this FileSuggestion.


        :param suggested: The suggested of this FileSuggestion.  # noqa: E501
        :type: dict(str, bool)
        """

        self._suggested = suggested


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
        if not isinstance(other, FileSuggestion):
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
