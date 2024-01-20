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

class GcpStorage(object):

    swagger_types = {
        'region': 'str',
        'bucket': 'str',
        'path': 'str',
        'zone': 'str',
        'config_type': 'str',
        'config_class': 'str'
    }

    attribute_map = {
        'region': 'region',
        'bucket': 'bucket',
        'path': 'path',
        'zone': 'zone',
        'config_type': 'config_type',
        'config_class': 'config_class'
    }

    rattribute_map = {
        'region': 'region',
        'bucket': 'bucket',
        'path': 'path',
        'zone': 'zone',
        'config_type': 'config_type',
        'config_class': 'config_class'
    }

    def __init__(self, region='us-central1', bucket=None, path='', zone=None, config_type=None, config_class=None):  # noqa: E501
        """GcpStorage - a model defined in Swagger"""
        super(GcpStorage, self).__init__()

        self._region = None
        self._bucket = None
        self._path = None
        self._zone = None
        self._config_type = None
        self._config_class = None
        self.discriminator = None
        self.alt_discriminator = None

        if region is not None:
            self.region = region
        self.bucket = bucket
        if path is not None:
            self.path = path
        if zone is not None:
            self.zone = zone
        if config_type is not None:
            self.config_type = config_type
        if config_class is not None:
            self.config_class = config_class

    @property
    def region(self):
        """Gets the region of this GcpStorage.


        :return: The region of this GcpStorage.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this GcpStorage.


        :param region: The region of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def bucket(self):
        """Gets the bucket of this GcpStorage.


        :return: The bucket of this GcpStorage.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this GcpStorage.


        :param bucket: The bucket of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._bucket = bucket

    @property
    def path(self):
        """Gets the path of this GcpStorage.


        :return: The path of this GcpStorage.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this GcpStorage.


        :param path: The path of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def zone(self):
        """Gets the zone of this GcpStorage.


        :return: The zone of this GcpStorage.
        :rtype: str
        """
        return self._zone

    @zone.setter
    def zone(self, zone):
        """Sets the zone of this GcpStorage.


        :param zone: The zone of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._zone = zone

    @property
    def config_type(self):
        """Gets the config_type of this GcpStorage.


        :return: The config_type of this GcpStorage.
        :rtype: str
        """
        return self._config_type

    @config_type.setter
    def config_type(self, config_type):
        """Sets the config_type of this GcpStorage.


        :param config_type: The config_type of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._config_type = config_type

    @property
    def config_class(self):
        """Gets the config_class of this GcpStorage.


        :return: The config_class of this GcpStorage.
        :rtype: str
        """
        return self._config_class

    @config_class.setter
    def config_class(self, config_class):
        """Sets the config_class of this GcpStorage.


        :param config_class: The config_class of this GcpStorage.  # noqa: E501
        :type: str
        """

        self._config_class = config_class


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
        if not isinstance(other, GcpStorage):
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
