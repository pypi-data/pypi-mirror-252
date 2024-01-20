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

class ReportGroupReport(object):

    swagger_types = {
        'project_count': 'int',
        'label': 'str',
        'session_count': 'int'
    }

    attribute_map = {
        'project_count': 'project_count',
        'label': 'label',
        'session_count': 'session_count'
    }

    rattribute_map = {
        'project_count': 'project_count',
        'label': 'label',
        'session_count': 'session_count'
    }

    def __init__(self, project_count=None, label=None, session_count=None):  # noqa: E501
        """ReportGroupReport - a model defined in Swagger"""
        super(ReportGroupReport, self).__init__()

        self._project_count = None
        self._label = None
        self._session_count = None
        self.discriminator = None
        self.alt_discriminator = None

        self.project_count = project_count
        self.label = label
        self.session_count = session_count

    @property
    def project_count(self):
        """Gets the project_count of this ReportGroupReport.


        :return: The project_count of this ReportGroupReport.
        :rtype: int
        """
        return self._project_count

    @project_count.setter
    def project_count(self, project_count):
        """Sets the project_count of this ReportGroupReport.


        :param project_count: The project_count of this ReportGroupReport.  # noqa: E501
        :type: int
        """

        self._project_count = project_count

    @property
    def label(self):
        """Gets the label of this ReportGroupReport.

        The group label

        :return: The label of this ReportGroupReport.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ReportGroupReport.

        The group label

        :param label: The label of this ReportGroupReport.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def session_count(self):
        """Gets the session_count of this ReportGroupReport.


        :return: The session_count of this ReportGroupReport.
        :rtype: int
        """
        return self._session_count

    @session_count.setter
    def session_count(self, session_count):
        """Sets the session_count of this ReportGroupReport.


        :param session_count: The session_count of this ReportGroupReport.  # noqa: E501
        :type: int
        """

        self._session_count = session_count


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
        if not isinstance(other, ReportGroupReport):
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
