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

from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.job_file_object_list_output import JobFileObjectListOutput  # noqa: F401,E501
from flywheel.models.location import Location  # noqa: F401,E501

class JobFileInputListOutput(object):

    swagger_types = {
        'hierarchy': 'ContainerReference',
        'object': 'JobFileObjectListOutput',
        'location': 'Location',
        'base': 'str'
    }

    attribute_map = {
        'hierarchy': 'hierarchy',
        'object': 'object',
        'location': 'location',
        'base': 'base'
    }

    rattribute_map = {
        'hierarchy': 'hierarchy',
        'object': 'object',
        'location': 'location',
        'base': 'base'
    }

    def __init__(self, hierarchy=None, object=None, location=None, base=None):  # noqa: E501
        """JobFileInputListOutput - a model defined in Swagger"""
        super(JobFileInputListOutput, self).__init__()

        self._hierarchy = None
        self._object = None
        self._location = None
        self._base = None
        self.discriminator = None
        self.alt_discriminator = None

        self.hierarchy = hierarchy
        self.object = object
        self.location = location
        if base is not None:
            self.base = base

    @property
    def hierarchy(self):
        """Gets the hierarchy of this JobFileInputListOutput.


        :return: The hierarchy of this JobFileInputListOutput.
        :rtype: ContainerReference
        """
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, hierarchy):
        """Sets the hierarchy of this JobFileInputListOutput.


        :param hierarchy: The hierarchy of this JobFileInputListOutput.  # noqa: E501
        :type: ContainerReference
        """

        self._hierarchy = hierarchy

    @property
    def object(self):
        """Gets the object of this JobFileInputListOutput.


        :return: The object of this JobFileInputListOutput.
        :rtype: JobFileObjectListOutput
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this JobFileInputListOutput.


        :param object: The object of this JobFileInputListOutput.  # noqa: E501
        :type: JobFileObjectListOutput
        """

        self._object = object

    @property
    def location(self):
        """Gets the location of this JobFileInputListOutput.


        :return: The location of this JobFileInputListOutput.
        :rtype: Location
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this JobFileInputListOutput.


        :param location: The location of this JobFileInputListOutput.  # noqa: E501
        :type: Location
        """

        self._location = location

    @property
    def base(self):
        """Gets the base of this JobFileInputListOutput.


        :return: The base of this JobFileInputListOutput.
        :rtype: str
        """
        return self._base

    @base.setter
    def base(self, base):
        """Sets the base of this JobFileInputListOutput.


        :param base: The base of this JobFileInputListOutput.  # noqa: E501
        :type: str
        """

        self._base = base


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
        if not isinstance(other, JobFileInputListOutput):
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
