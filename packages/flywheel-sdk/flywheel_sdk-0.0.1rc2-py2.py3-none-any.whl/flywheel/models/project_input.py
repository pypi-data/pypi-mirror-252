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

from flywheel.models.edition import Edition  # noqa: F401,E501
from flywheel.models.ldap_sync_config import LdapSyncConfig  # noqa: F401,E501
from flywheel.models.providers import Providers  # noqa: F401,E501
from flywheel.models.role_permission import RolePermission  # noqa: F401,E501

class ProjectInput(object):

    swagger_types = {
        'label': 'str',
        'description': 'str',
        'group': 'str',
        'editions': 'Edition',
        'providers': 'Providers',
        'ldap_sync': 'LdapSyncConfig',
        'permissions': 'list[RolePermission]',
        'copyable': 'bool',
        'info': 'object'
    }

    attribute_map = {
        'label': 'label',
        'description': 'description',
        'group': 'group',
        'editions': 'editions',
        'providers': 'providers',
        'ldap_sync': 'ldap_sync',
        'permissions': 'permissions',
        'copyable': 'copyable',
        'info': 'info'
    }

    rattribute_map = {
        'label': 'label',
        'description': 'description',
        'group': 'group',
        'editions': 'editions',
        'providers': 'providers',
        'ldap_sync': 'ldap_sync',
        'permissions': 'permissions',
        'copyable': 'copyable',
        'info': 'info'
    }

    def __init__(self, label=None, description='', group=None, editions=None, providers=None, ldap_sync=None, permissions=None, copyable=None, info=None):  # noqa: E501
        """ProjectInput - a model defined in Swagger"""
        super(ProjectInput, self).__init__()

        self._label = None
        self._description = None
        self._group = None
        self._editions = None
        self._providers = None
        self._ldap_sync = None
        self._permissions = None
        self._copyable = None
        self._info = None
        self.discriminator = None
        self.alt_discriminator = None

        self.label = label
        if description is not None:
            self.description = description
        self.group = group
        if editions is not None:
            self.editions = editions
        if providers is not None:
            self.providers = providers
        if ldap_sync is not None:
            self.ldap_sync = ldap_sync
        if permissions is not None:
            self.permissions = permissions
        if copyable is not None:
            self.copyable = copyable
        if info is not None:
            self.info = info

    @property
    def label(self):
        """Gets the label of this ProjectInput.


        :return: The label of this ProjectInput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ProjectInput.


        :param label: The label of this ProjectInput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def description(self):
        """Gets the description of this ProjectInput.


        :return: The description of this ProjectInput.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ProjectInput.


        :param description: The description of this ProjectInput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def group(self):
        """Gets the group of this ProjectInput.


        :return: The group of this ProjectInput.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this ProjectInput.


        :param group: The group of this ProjectInput.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def editions(self):
        """Gets the editions of this ProjectInput.


        :return: The editions of this ProjectInput.
        :rtype: Edition
        """
        return self._editions

    @editions.setter
    def editions(self, editions):
        """Sets the editions of this ProjectInput.


        :param editions: The editions of this ProjectInput.  # noqa: E501
        :type: Edition
        """

        self._editions = editions

    @property
    def providers(self):
        """Gets the providers of this ProjectInput.


        :return: The providers of this ProjectInput.
        :rtype: Providers
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this ProjectInput.


        :param providers: The providers of this ProjectInput.  # noqa: E501
        :type: Providers
        """

        self._providers = providers

    @property
    def ldap_sync(self):
        """Gets the ldap_sync of this ProjectInput.


        :return: The ldap_sync of this ProjectInput.
        :rtype: LdapSyncConfig
        """
        return self._ldap_sync

    @ldap_sync.setter
    def ldap_sync(self, ldap_sync):
        """Sets the ldap_sync of this ProjectInput.


        :param ldap_sync: The ldap_sync of this ProjectInput.  # noqa: E501
        :type: LdapSyncConfig
        """

        self._ldap_sync = ldap_sync

    @property
    def permissions(self):
        """Gets the permissions of this ProjectInput.


        :return: The permissions of this ProjectInput.
        :rtype: list[RolePermission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ProjectInput.


        :param permissions: The permissions of this ProjectInput.  # noqa: E501
        :type: list[RolePermission]
        """

        self._permissions = permissions

    @property
    def copyable(self):
        """Gets the copyable of this ProjectInput.


        :return: The copyable of this ProjectInput.
        :rtype: bool
        """
        return self._copyable

    @copyable.setter
    def copyable(self, copyable):
        """Sets the copyable of this ProjectInput.


        :param copyable: The copyable of this ProjectInput.  # noqa: E501
        :type: bool
        """

        self._copyable = copyable

    @property
    def info(self):
        """Gets the info of this ProjectInput.


        :return: The info of this ProjectInput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this ProjectInput.


        :param info: The info of this ProjectInput.  # noqa: E501
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
        if not isinstance(other, ProjectInput):
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
