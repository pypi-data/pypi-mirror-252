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

from flywheel.models.form_definition import FormDefinition  # noqa: F401,E501
from flywheel.models.project_settings_sharing_input import ProjectSettingsSharingInput  # noqa: F401,E501
from flywheel.models.project_settings_workspaces_input import ProjectSettingsWorkspacesInput  # noqa: F401,E501
from flywheel.models.viewer_app import ViewerApp  # noqa: F401,E501

class ProjectSettingsInput(object):

    swagger_types = {
        'viewer_apps': 'list[ViewerApp]',
        'deid_profile': 'union[string,object]',
        'forms': 'dict(str, list[FormDefinition])',
        'external_routing_id': 'str',
        'sharing': 'ProjectSettingsSharingInput',
        'workspaces': 'ProjectSettingsWorkspacesInput'
    }

    attribute_map = {
        'viewer_apps': 'viewer_apps',
        'deid_profile': 'deid_profile',
        'forms': 'forms',
        'external_routing_id': 'external_routing_id',
        'sharing': 'sharing',
        'workspaces': 'workspaces'
    }

    rattribute_map = {
        'viewer_apps': 'viewer_apps',
        'deid_profile': 'deid_profile',
        'forms': 'forms',
        'external_routing_id': 'external_routing_id',
        'sharing': 'sharing',
        'workspaces': 'workspaces'
    }

    def __init__(self, viewer_apps=None, deid_profile=None, forms=None, external_routing_id=None, sharing=None, workspaces=None):  # noqa: E501
        """ProjectSettingsInput - a model defined in Swagger"""
        super(ProjectSettingsInput, self).__init__()

        self._viewer_apps = None
        self._deid_profile = None
        self._forms = None
        self._external_routing_id = None
        self._sharing = None
        self._workspaces = None
        self.discriminator = None
        self.alt_discriminator = None

        if viewer_apps is not None:
            self.viewer_apps = viewer_apps
        if deid_profile is not None:
            self.deid_profile = deid_profile
        if forms is not None:
            self.forms = forms
        if external_routing_id is not None:
            self.external_routing_id = external_routing_id
        if sharing is not None:
            self.sharing = sharing
        if workspaces is not None:
            self.workspaces = workspaces

    @property
    def viewer_apps(self):
        """Gets the viewer_apps of this ProjectSettingsInput.


        :return: The viewer_apps of this ProjectSettingsInput.
        :rtype: list[ViewerApp]
        """
        return self._viewer_apps

    @viewer_apps.setter
    def viewer_apps(self, viewer_apps):
        """Sets the viewer_apps of this ProjectSettingsInput.


        :param viewer_apps: The viewer_apps of this ProjectSettingsInput.  # noqa: E501
        :type: list[ViewerApp]
        """

        self._viewer_apps = viewer_apps

    @property
    def deid_profile(self):
        """Gets the deid_profile of this ProjectSettingsInput.


        :return: The deid_profile of this ProjectSettingsInput.
        :rtype: union[string,object]
        """
        return self._deid_profile

    @deid_profile.setter
    def deid_profile(self, deid_profile):
        """Sets the deid_profile of this ProjectSettingsInput.


        :param deid_profile: The deid_profile of this ProjectSettingsInput.  # noqa: E501
        :type: union[string,object]
        """

        self._deid_profile = deid_profile

    @property
    def forms(self):
        """Gets the forms of this ProjectSettingsInput.


        :return: The forms of this ProjectSettingsInput.
        :rtype: dict(str, list[FormDefinition])
        """
        return self._forms

    @forms.setter
    def forms(self, forms):
        """Sets the forms of this ProjectSettingsInput.


        :param forms: The forms of this ProjectSettingsInput.  # noqa: E501
        :type: dict(str, list[FormDefinition])
        """

        self._forms = forms

    @property
    def external_routing_id(self):
        """Gets the external_routing_id of this ProjectSettingsInput.


        :return: The external_routing_id of this ProjectSettingsInput.
        :rtype: str
        """
        return self._external_routing_id

    @external_routing_id.setter
    def external_routing_id(self, external_routing_id):
        """Sets the external_routing_id of this ProjectSettingsInput.


        :param external_routing_id: The external_routing_id of this ProjectSettingsInput.  # noqa: E501
        :type: str
        """

        self._external_routing_id = external_routing_id

    @property
    def sharing(self):
        """Gets the sharing of this ProjectSettingsInput.


        :return: The sharing of this ProjectSettingsInput.
        :rtype: ProjectSettingsSharingInput
        """
        return self._sharing

    @sharing.setter
    def sharing(self, sharing):
        """Sets the sharing of this ProjectSettingsInput.


        :param sharing: The sharing of this ProjectSettingsInput.  # noqa: E501
        :type: ProjectSettingsSharingInput
        """

        self._sharing = sharing

    @property
    def workspaces(self):
        """Gets the workspaces of this ProjectSettingsInput.


        :return: The workspaces of this ProjectSettingsInput.
        :rtype: ProjectSettingsWorkspacesInput
        """
        return self._workspaces

    @workspaces.setter
    def workspaces(self, workspaces):
        """Sets the workspaces of this ProjectSettingsInput.


        :param workspaces: The workspaces of this ProjectSettingsInput.  # noqa: E501
        :type: ProjectSettingsWorkspacesInput
        """

        self._workspaces = workspaces


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
        if not isinstance(other, ProjectSettingsInput):
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
