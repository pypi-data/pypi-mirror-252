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

class TreeGraphConnection(object):

    swagger_types = {
        'local': 'str',
        'foreign': 'str',
        'collection': 'str',
        'order': 'str'
    }

    attribute_map = {
        'local': 'local',
        'foreign': 'foreign',
        'collection': 'collection',
        'order': 'order'
    }

    rattribute_map = {
        'local': 'local',
        'foreign': 'foreign',
        'collection': 'collection',
        'order': 'order'
    }

    def __init__(self, local=None, foreign=None, collection=None, order=None):  # noqa: E501
        """TreeGraphConnection - a model defined in Swagger"""
        super(TreeGraphConnection, self).__init__()

        self._local = None
        self._foreign = None
        self._collection = None
        self._order = None
        self.discriminator = None
        self.alt_discriminator = None

        if local is not None:
            self.local = local
        self.foreign = foreign
        if collection is not None:
            self.collection = collection
        if order is not None:
            self.order = order

    @property
    def local(self):
        """Gets the local of this TreeGraphConnection.


        :return: The local of this TreeGraphConnection.
        :rtype: str
        """
        return self._local

    @local.setter
    def local(self, local):
        """Sets the local of this TreeGraphConnection.


        :param local: The local of this TreeGraphConnection.  # noqa: E501
        :type: str
        """

        self._local = local

    @property
    def foreign(self):
        """Gets the foreign of this TreeGraphConnection.


        :return: The foreign of this TreeGraphConnection.
        :rtype: str
        """
        return self._foreign

    @foreign.setter
    def foreign(self, foreign):
        """Sets the foreign of this TreeGraphConnection.


        :param foreign: The foreign of this TreeGraphConnection.  # noqa: E501
        :type: str
        """

        self._foreign = foreign

    @property
    def collection(self):
        """Gets the collection of this TreeGraphConnection.


        :return: The collection of this TreeGraphConnection.
        :rtype: str
        """
        return self._collection

    @collection.setter
    def collection(self, collection):
        """Sets the collection of this TreeGraphConnection.


        :param collection: The collection of this TreeGraphConnection.  # noqa: E501
        :type: str
        """

        self._collection = collection

    @property
    def order(self):
        """Gets the order of this TreeGraphConnection.


        :return: The order of this TreeGraphConnection.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this TreeGraphConnection.


        :param order: The order of this TreeGraphConnection.  # noqa: E501
        :type: str
        """

        self._order = order


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
        if not isinstance(other, TreeGraphConnection):
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
