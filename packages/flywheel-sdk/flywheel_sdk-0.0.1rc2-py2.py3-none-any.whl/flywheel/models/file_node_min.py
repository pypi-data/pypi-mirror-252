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

class FileNodeMin(object):

    swagger_types = {
        'id': 'str',
        'name': 'str',
        'size': 'int',
        'created': 'datetime',
        'modified': 'datetime',
        'container_type': 'str',
        'node_type': 'str'
    }

    attribute_map = {
        'id': '_id',
        'name': 'name',
        'size': 'size',
        'created': 'created',
        'modified': 'modified',
        'container_type': 'container_type',
        'node_type': 'node_type'
    }

    rattribute_map = {
        '_id': 'id',
        'name': 'name',
        'size': 'size',
        'created': 'created',
        'modified': 'modified',
        'container_type': 'container_type',
        'node_type': 'node_type'
    }

    def __init__(self, id=None, name=None, size=None, created=None, modified=None, container_type='file', node_type='file'):  # noqa: E501
        """FileNodeMin - a model defined in Swagger"""
        super(FileNodeMin, self).__init__()

        self._id = None
        self._name = None
        self._size = None
        self._created = None
        self._modified = None
        self._container_type = None
        self._node_type = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        self.name = name
        self.size = size
        self.created = created
        self.modified = modified
        if container_type is not None:
            self.container_type = container_type
        if node_type is not None:
            self.node_type = node_type

    @property
    def id(self):
        """Gets the id of this FileNodeMin.


        :return: The id of this FileNodeMin.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FileNodeMin.


        :param id: The id of this FileNodeMin.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this FileNodeMin.


        :return: The name of this FileNodeMin.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FileNodeMin.


        :param name: The name of this FileNodeMin.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def size(self):
        """Gets the size of this FileNodeMin.


        :return: The size of this FileNodeMin.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FileNodeMin.


        :param size: The size of this FileNodeMin.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def created(self):
        """Gets the created of this FileNodeMin.


        :return: The created of this FileNodeMin.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this FileNodeMin.


        :param created: The created of this FileNodeMin.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this FileNodeMin.


        :return: The modified of this FileNodeMin.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this FileNodeMin.


        :param modified: The modified of this FileNodeMin.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def container_type(self):
        """Gets the container_type of this FileNodeMin.


        :return: The container_type of this FileNodeMin.
        :rtype: str
        """
        return self._container_type

    @container_type.setter
    def container_type(self, container_type):
        """Sets the container_type of this FileNodeMin.


        :param container_type: The container_type of this FileNodeMin.  # noqa: E501
        :type: str
        """

        self._container_type = container_type

    @property
    def node_type(self):
        """Gets the node_type of this FileNodeMin.


        :return: The node_type of this FileNodeMin.
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this FileNodeMin.


        :param node_type: The node_type of this FileNodeMin.  # noqa: E501
        :type: str
        """

        self._node_type = node_type


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
        if not isinstance(other, FileNodeMin):
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
