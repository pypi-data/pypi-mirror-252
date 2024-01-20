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

from flywheel.models.core_models_source_source import CoreModelsSourceSource  # noqa: F401,E501

class AcquisitionUpsertInput(object):

    swagger_types = {
        'id': 'str',
        'uid': 'str',
        'routing_field': 'str',
        'label': 'str',
        'source': 'CoreModelsSourceSource',
        'timestamp': 'datetime',
        'timezone': 'str',
        'info': 'object'
    }

    attribute_map = {
        'id': '_id',
        'uid': 'uid',
        'routing_field': 'routing_field',
        'label': 'label',
        'source': 'source',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'info': 'info'
    }

    rattribute_map = {
        '_id': 'id',
        'uid': 'uid',
        'routing_field': 'routing_field',
        'label': 'label',
        'source': 'source',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'info': 'info'
    }

    def __init__(self, id=None, uid=None, routing_field=None, label=None, source=None, timestamp=None, timezone=None, info=None):  # noqa: E501
        """AcquisitionUpsertInput - a model defined in Swagger"""
        super(AcquisitionUpsertInput, self).__init__()

        self._id = None
        self._uid = None
        self._routing_field = None
        self._label = None
        self._source = None
        self._timestamp = None
        self._timezone = None
        self._info = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if uid is not None:
            self.uid = uid
        if routing_field is not None:
            self.routing_field = routing_field
        if label is not None:
            self.label = label
        if source is not None:
            self.source = source
        if timestamp is not None:
            self.timestamp = timestamp
        if timezone is not None:
            self.timezone = timezone
        if info is not None:
            self.info = info

    @property
    def id(self):
        """Gets the id of this AcquisitionUpsertInput.


        :return: The id of this AcquisitionUpsertInput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AcquisitionUpsertInput.


        :param id: The id of this AcquisitionUpsertInput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def uid(self):
        """Gets the uid of this AcquisitionUpsertInput.


        :return: The uid of this AcquisitionUpsertInput.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this AcquisitionUpsertInput.


        :param uid: The uid of this AcquisitionUpsertInput.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def routing_field(self):
        """Gets the routing_field of this AcquisitionUpsertInput.


        :return: The routing_field of this AcquisitionUpsertInput.
        :rtype: str
        """
        return self._routing_field

    @routing_field.setter
    def routing_field(self, routing_field):
        """Sets the routing_field of this AcquisitionUpsertInput.


        :param routing_field: The routing_field of this AcquisitionUpsertInput.  # noqa: E501
        :type: str
        """

        self._routing_field = routing_field

    @property
    def label(self):
        """Gets the label of this AcquisitionUpsertInput.


        :return: The label of this AcquisitionUpsertInput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AcquisitionUpsertInput.


        :param label: The label of this AcquisitionUpsertInput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def source(self):
        """Gets the source of this AcquisitionUpsertInput.


        :return: The source of this AcquisitionUpsertInput.
        :rtype: CoreModelsSourceSource
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this AcquisitionUpsertInput.


        :param source: The source of this AcquisitionUpsertInput.  # noqa: E501
        :type: CoreModelsSourceSource
        """

        self._source = source

    @property
    def timestamp(self):
        """Gets the timestamp of this AcquisitionUpsertInput.


        :return: The timestamp of this AcquisitionUpsertInput.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this AcquisitionUpsertInput.


        :param timestamp: The timestamp of this AcquisitionUpsertInput.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def timezone(self):
        """Gets the timezone of this AcquisitionUpsertInput.


        :return: The timezone of this AcquisitionUpsertInput.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this AcquisitionUpsertInput.


        :param timezone: The timezone of this AcquisitionUpsertInput.  # noqa: E501
        :type: str
        """

        self._timezone = timezone

    @property
    def info(self):
        """Gets the info of this AcquisitionUpsertInput.


        :return: The info of this AcquisitionUpsertInput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this AcquisitionUpsertInput.


        :param info: The info of this AcquisitionUpsertInput.  # noqa: E501
        :type: object
        """

        self._info = info


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
        if not isinstance(other, AcquisitionUpsertInput):
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
